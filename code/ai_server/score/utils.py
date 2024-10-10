


import random
import numpy as np









def get_straight_goal(x_list_source,y_list_source,straight_score):
    x_list = y_list_source
    y_list = x_list_source
    
    straight_score = round(straight_score,4)
    x_forward = { 'score':0,'comment':''}
    x_back = { 'score':0,'comment':''}
    y_forward = { 'score':0,'comment':''}
    y_back = { 'score':0,'comment':''}
    
    if len(x_list)>0:
        
        
        #x_list 颠倒
        print ('x_0:',x_list[-1])
        print ('x_-1:',x_list[0])
        
        if x_list[-1] - x_list[0] < 0 :
            x_forward['score'] = 1
            x_forward['comment'] = 'x轴正转正确，'
            x_back['comment'] = 'x轴反转错误，'
        else:
            x_back['score'] = 1
            x_forward['comment'] = 'x轴正转错误，'
            x_back['comment'] = 'x轴反转正确，'
            
    if len(y_list)>0:
        
        #x_list 颠倒
        print ('y_0:',y_list[-1])
        print ('y_-1:',y_list[0])
        
        if y_list[-1] - y_list[0] < 0 :
            y_forward['score'] = 1
            y_forward['comment'] = 'y轴正转正确，'
            y_back['comment'] = 'y轴反转错误，'
        else:
            y_back['score'] = 1
            y_forward['comment'] = 'y轴正转错误，'
            y_back['comment'] = 'y轴反转正确，'
    
    if straight_score>0.9:
        straight_comment = '直线运行成功，太棒了！'
    else:
        straight_comment = '直线运行失败，需要改正！'
    
    
    if x_forward['score'] == 1:        
        x_forward['score'] = straight_score
        x_forward['comment']+=straight_comment
    else:
        x_forward['comment']+='需要改正方向！'
        
    if x_back['score'] == 1:        
        x_back['score'] = straight_score
        x_back['comment']+=straight_comment
    else:
        x_back['comment']+='需要改正方向！'
        
    
    if y_forward['score'] == 1:        
        y_forward['score'] = straight_score
        y_forward['comment']+=straight_comment
    else:
        y_forward['comment']+='需要改正方向！'

    if y_back['score'] == 1:        
        y_back['score'] = straight_score
        y_back['comment']+=straight_comment
    else:
        y_back['comment']+='需要改正方向！'

    x_forward['score'] = str(x_forward['score'])
    y_forward['score'] = str(y_forward['score'])
    x_back['score'] = str(x_back['score'])
    y_back['score'] = str(y_back['score'])
    
    return x_forward,x_back,y_forward,y_back



def random_num(num):

    random_list_1d = [random.randint(50, 100) for _ in range(num)]
    return random_list_1d


def comment(score):

    phrases_1 = ["知识点掌握的很牢", "对知识了解的很透彻", "知识掌握的很好"]
    phrases_2 = ["对知识点的理解尚可", "对知识的掌握上表现良好", "知识掌握的一般"]
    phrases_3 = ["对知识点的掌握不够扎实", "对知识的理解不到位", "知识掌握的较差"]

    if score>=8:
        return random.choice(phrases_1)
    elif 8>score>=6:
        return random.choice(phrases_2)
    return random.choice(phrases_3)


def jungement(num):

    jungement_dict = {
    }
    scores = random_num(num)
    jungement_dict["scores"] = scores
    commentword = []
    for i in range(len(scores)):
        word = comment(scores[i])
        commentword.append(word)
    jungement_dict["comment"] = commentword

    return jungement_dict



from shapely.geometry import LineString,Point
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient


def get_straight_trajectory_LIP(traj,show=False):
    if len(traj)<3:
        return 0
    
    #env = EnvConfig()
    #if Point(traj[0]).distance(Point(traj[-1]))< env.same_point_threshold:
    #    return 0
    
    deviation = 0
    target_traj = []
    target_traj.append(traj[0])
    target_traj.append(traj[-1])
    
    '''
    if show:
        # 创建图形和轴  
        fig, ax = plt.subplots()
        # 将轨迹点转换为NumPy数组以使用matplotlib进行绘图  
        traj_np = np.array(traj)  
        target_traj_np = np.array(target_traj)
        # 绘制目标轨迹（实线）  
        ax.plot(target_traj_np[:, 0], target_traj_np[:, 1], 'r-o', label='Target Trajectory')  
        # 绘制原始轨迹（虚线）  
        ax.plot(traj_np[:, 0], traj_np[:, 1], 'b--o', label='Original Trajectory')  
    '''
    
    traj_linestr = LineString(traj)
    target_linestr = LineString(target_traj)
    
    for p_i in range(len(traj_linestr.coords)-1):
        if p_i == 0:
            continue
        
        length1 = Point(traj_linestr.coords[p_i-1]).distance(Point(traj_linestr.coords[p_i]))
        length2 = Point(traj_linestr.coords[p_i+1]).distance(Point(traj_linestr.coords[p_i]))
        weight = (length1+length2)/traj_linestr.length
        dist = target_linestr.distance(Point(traj_linestr.coords[p_i]))
        deviation += weight * dist
        
        
        '''
        if show:
            # 计算垂足  
            nearest_point = target_linestr.interpolate(target_linestr.project(Point(traj[p_i])))  
            x_perp, y_perp = nearest_point.xy  
            # 绘制垂线  
            ax.plot([traj[p_i][0], x_perp[0]], [traj[p_i][1], y_perp[0]], 'g--', alpha=0.5)
            # 标注距离 
            ax.annotate(f'{dist:.6f}', (traj[p_i][0],traj[p_i][1]), textcoords="offset points",  xytext=(0,10), ha='center')
        '''
    
    score = max(1 - deviation / target_linestr.length,0)
    
    '''
    if env.log_print_level>2:
        print ('straight line score:',score)
        
    if show:
        #ax.legend()
        plt.show()
    '''
    return score



def str_array2np_array_float(str_array):
    # 移除字符串两端的方括号  
    cleaned_str = str_array[1:-1]  
    # 使用逗号分割字符串，得到每个元素的字符串表示  
    elements_str = cleaned_str.split(',')  
    # 将每个元素的字符串表示转换为浮点数  
    elements_float = [float(x) for x in elements_str]  
    # 使用NumPy的array函数将列表转换为数组  
    array_back = np.array(elements_float)  
    #print(array_back)  
    return array_back