

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    #model='model/iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch')
    model=r'F:\workspace\majun\zhiyuanchuang_space\model_endpoints\voice_word\speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch')

#rec_result = inference_pipeline("D:/jrr/Jproject/Insect-Pest-Recognition/voice_rec/model/iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch\example/asr_example.wav")
rec_result = inference_pipeline(r"F:\workspace\majun\zhiyuanchuang_space\model_endpoints\voice_word\speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch\example\asr_example.wav")
print(rec_result)