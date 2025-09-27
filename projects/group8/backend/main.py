from fastapi import FastAPI, Form, UploadFile, File
from typing import List
import uuid
from services import llm, whisper_service, vision, slang_crawler, stats, user_profile, speech
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/language_quiz/")
def language_quiz(lang: str = Form(...)):
    """AI自动出选择题"""
    return llm.generate_quiz(lang)

@app.post("/api/language_quiz_grade/")
def language_quiz_grade(lang: str = Form(...), level: int = Form(...), user_answers: str = Form(None), quiz_payload: str = Form(None)):
    """AI根据用户选择题答案评级，支持quiz_payload（含题目、答案、作答）"""
    import json
    if quiz_payload:
        payload = json.loads(quiz_payload)
        return llm.grade_quiz(lang, level, payload)
    else:
        return llm.grade_quiz(lang, level, user_answers)


@app.post("/api/correct_sentence/")
def correct_sentence(sentence: str = Form(...), lang: str = Form(...), native_lang: str = Form(...)):
    """句子实时纠错"""
    return llm.correct_sentence(sentence, lang, native_lang)

# 在 main.py 中添加
@app.post("/api/describe_image/")
def describe_image(
    image_urls: List[str] = Form(...),
    prompt: str = Form("请用一句话描述图片内容")
):
    vision_result = vision.describe(image_urls, prompt)
    return vision_result

@app.post("/api/generate_slang/")
def generate_slang(topic: str = Form(...), lang: str = Form(...), native_lang: str = Form(...)):
    """俚语生成"""
    return llm.generate_slang(topic, lang, native_lang)

@app.post("/api/generate_vocab/")
def generate_vocab(lang: str = Form(...), level: int = Form(...)):
    return llm.generate_vocab(lang, level)

@app.post("/api/generate_story/")
def generate_story(lang: str = Form(...), level: int = Form(...), vocab: str = Form(...)):
    vocab_list = json.loads(vocab)
    return llm.generate_story(lang, level, vocab_list)

@app.post("/api/extract_grammar/")
def extract_grammar(lang: str = Form(...), story: str = Form(...)):
    return llm.extract_grammar(lang, story)

# @app.post("/api/speech_to_text/")
# def speech_to_text(file: UploadFile = File(...)):
#     """语音识别"""
#     return whisper.speech_to_text(file.file.read())

@app.post("/api/user_stats/")
def user_stats(user_id: str = Form(...)):
    """用户错误统计分析"""
    return stats.get_user_stats(user_id) 

@app.post("/api/register_user/")
def api_register_user(user_id: str = Form(...), info: str = Form(...)):
    """注册用户，info为json字符串"""
    import json
    info_dict = json.loads(info)
    return user_profile.register_user(user_id, info_dict)

@app.post("/api/get_user_profile/")
def api_get_user_profile(user_id: str = Form(...)):
    """获取用户档案"""
    return user_profile.get_user_profile(user_id)

@app.post("/api/update_user_profile/")
def api_update_user_profile(user_id: str = Form(...), updates: str = Form(...)):
    """更新用户档案，updates为json字符串"""
    import json
    updates_dict = json.loads(updates)
    return user_profile.update_user_profile(user_id, updates_dict)

@app.post("/api/add_history/")
def api_add_history(user_id: str = Form(...), module: str = Form(...), record: str = Form(...)):
    """添加用户历史记录，record为json字符串，module如'tests','corrections','slang','vision'"""
    import json
    record_dict = json.loads(record)
    return user_profile.add_history(user_id, module, record_dict) 

@app.post("/api/role_chat/")
def role_chat(lang: str = Form(...), role: str = Form(...), history: str = Form(...)):
    import json
    history_list = json.loads(history)
    return llm.role_chat(lang, role, history_list) 

@app.post("/api/speech_recognize/")
def api_speech_recognize(audio_url: str = Form(...)):
    """语音识别API，接收音频公网URL，返回识别文本"""
    text = speech.speech_recognize(audio_url)
    return {"text": text}

@app.post("/api/speech_synthesize/")
def api_speech_synthesize(text: str = Form(...), voice: str = Form('Cherry'), slow: bool = Form(False)):
    """语音合成API，输入文本、音色等返回音频（base64编码）"""
    audio_bytes = speech.speech_synthesize(text, voice, slow)
    import base64
    audio_b64 = base64.b64encode(audio_bytes).decode()
    return {"audio_b64": audio_b64} 