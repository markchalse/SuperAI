from PIL import Image
from torchvision import transforms
import torch
from torch.autograd import Variable
import torch.nn as nn
from torch.nn.utils import fuse_conv_bn_eval
from torchvision import models
from torch.nn import init
import supervision as sv
import os
import cv2
import uuid
import time





def weights_init_kaiming(m):
    classname = m.__class__.__name__
    # print(classname)
    if classname.find('Conv') != -1:
        init.kaiming_normal_(m.weight.data, a=0, mode='fan_in') # For old pytorch, you may use kaiming_normal.
    elif classname.find('Linear') != -1:
        init.kaiming_normal_(m.weight.data, a=0, mode='fan_out')
    elif classname.find('BatchNorm1d') != -1:
        init.normal_(m.weight.data, 1.0, 0.02)
    if hasattr(m, 'bias') and m.bias is not None:
        init.constant_(m.bias.data, 0.0)

def weights_init_classifier(m):
    classname = m.__class__.__name__
    if classname.find('Linear') != -1:
        init.normal_(m.weight.data, std=0.001)
        init.constant_(m.bias.data, 0.0)

class ClassBlock(nn.Module):
    def __init__(self, input_dim, class_num, droprate, relu=False, bnorm=True, linear=512, return_f = False):
        super(ClassBlock, self).__init__()
        self.return_f = return_f
        add_block = []
        if linear>0:
            add_block += [nn.Linear(input_dim, linear)]
        else:
            linear = input_dim
        if bnorm:
            add_block += [nn.BatchNorm1d(linear)]
        if relu:
            add_block += [nn.LeakyReLU(0.1)]
        if droprate>0:
            add_block += [nn.Dropout(p=droprate)]
        add_block = nn.Sequential(*add_block)
        add_block.apply(weights_init_kaiming)

        classifier = []
        classifier += [nn.Linear(linear, class_num)]
        classifier = nn.Sequential(*classifier)
        classifier.apply(weights_init_classifier)

        self.add_block = add_block
        self.classifier = classifier
    def forward(self, x):
        x = self.add_block(x)
        if self.return_f:
            f = x
            x = self.classifier(x)
            return [x,f]
        else:
            x = self.classifier(x)
            return x

class ft_net(nn.Module):

    def __init__(self, class_num=751, droprate=0.5, stride=2, circle=False, ibn=False, linear_num=512):
        super(ft_net, self).__init__()
        model_ft = models.resnet50(pretrained=True)
        if ibn==True:
            model_ft = torch.hub.load('XingangPan/IBN-Net', 'resnet50_ibn_a', pretrained=True)
        # avg pooling to global pooling
        if stride == 1:
            model_ft.layer4[0].downsample[0].stride = (1,1)
            model_ft.layer4[0].conv2.stride = (1,1)
        model_ft.avgpool = nn.AdaptiveAvgPool2d((1,1))
        self.model = model_ft
        self.circle = circle
        self.classifier = ClassBlock(2048, class_num, droprate, linear=linear_num, return_f = circle)

    def forward(self, x):
        x = self.model.conv1(x)
        x = self.model.bn1(x)
        x = self.model.relu(x)
        x = self.model.maxpool(x)
        x = self.model.layer1(x)
        x = self.model.layer2(x)
        x = self.model.layer3(x)
        x = self.model.layer4(x)
        x = self.model.avgpool(x)
        x = x.view(x.size(0), x.size(1))
        x = self.classifier(x)
        return x

def load_network(network,model_path):
        network.load_state_dict(torch.load(model_path))
        return network
    
def fuse_all_conv_bn(model):
    stack = []
    for name, module in model.named_children():
        if list(module.named_children()):
            fuse_all_conv_bn(module)
            
        if isinstance(module, nn.BatchNorm2d):
            if not stack:
                continue
            if isinstance(stack[-1][1], nn.Conv2d):
                setattr(model, stack[-1][0], fuse_conv_bn_eval(stack[-1][1], module))
                setattr(model, name, nn.Identity())
        else:
            stack.append((name, module))
    return model


