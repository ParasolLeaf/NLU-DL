import os
import tempfile
import whisper as whisper_lib
import dashscope
import requests
import json
import time

DASHSCOPE_API_KEY = "sk-XXX"


def recognize_speech(audio_url, model_name='base'):
    """调用阿里云Paraformer语音识别API，使用传入的音频URL，自动拉取transcription_url获取最终识别文本。"""
    DASHSCOPE_API_KEY = "sk-XXX"
    file_urls = [audio_url]
    language_hints = ["zh", "en"]
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }
    data = {
        "model": "paraformer-v2",
        "input": {"file_urls": file_urls},
        "parameters": {"language_hints": language_hints},
    }
    service_url = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription"
    response = requests.post(service_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        task_id = response.json()["output"]["task_id"]
    else:
        raise RuntimeError(f"提交识别任务失败: {response.text}")
    # 轮询任务状态
    while True:
        status_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
        status_resp = requests.post(status_url, headers=headers)
        if status_resp.status_code == 200:
            status = status_resp.json()['output']['task_status']
            if status == 'SUCCEEDED':
                results = status_resp.json()['output']['results']
                print("阿里云ASR返回结果:", results)
                if results and isinstance(results, list):
                    result0 = results[0]
                    if 'transcription_url' in result0:
                        # 拉取最终识别结果
                        resp = requests.get(result0['transcription_url'])
                        if resp.status_code == 200:
                            data = resp.json()
                            # 只返回最终识别文本
                            if 'transcripts' in data and data['transcripts']:
                                return data['transcripts'][0].get('text', str(data['transcripts'][0]))
                            elif 'text' in data:
                                return data['text']
                            else:
                                return str(data)
                        else:
                            return f"拉取识别文本失败: {resp.text}"
                    elif 'text' in result0:
                        return result0['text']
                    else:
                        return str(result0)
                else:
                    return "未识别到有效文本，原始返回：" + str(results)
            elif status in ['RUNNING', 'PENDING']:
                time.sleep(0.5)
            else:
                raise RuntimeError(f"识别任务失败: {status_resp.text}")
        else:
            raise RuntimeError(f"查询任务失败: {status_resp.text}")


def synthesize_speech(text, voice='Cherry', slow=False):
    """调用阿里云Qwen-TTS进行语音合成，支持voice参数。"""
    DASHSCOPE_API_KEY = "sk-XXX"
    response = dashscope.audio.qwen_tts.SpeechSynthesizer.call(
        model="qwen-tts",
        api_key=DASHSCOPE_API_KEY,
        text=text,
        voice=voice
    )
    audio_url = response['output']['audio']['url']
    audio_resp = requests.get(audio_url)
    audio_resp.raise_for_status()
    return audio_resp.content