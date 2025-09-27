from . import whisper_service

def speech_recognize(audio_url, model_name='base'):
    """语音识别：音频URL转文本"""
    return whisper_service.recognize_speech(audio_url, model_name)


def speech_synthesize(text, voice='Cherry', slow=False):
    """语音合成：文本转音频，支持voice参数"""
    return whisper_service.synthesize_speech(text, voice, slow) 