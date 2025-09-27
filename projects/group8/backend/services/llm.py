import os
import httpx
from services import slang_crawler

# 请更新为有效的API Key
DOUBAO_API_KEY = ""  # 需要更新
BAIDU_API_KEY = ""  # 需要更新
ALI_API_KEY = ""

def call_doubao(prompt, model="ep-XXX"):
    try:
        resp = httpx.post(
            "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
            headers={
                "Authorization": f"Bearer {DOUBAO_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "你是人工智能助手."},
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=30
        )
        data = resp.json()
        if resp.status_code == 200 and "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        else:
            return f"豆包API异常: {data.get('error', {}).get('message', str(data))}"
    except Exception as e:
        return f"豆包API错误: {e}"

def call_baidu(prompt):
    try:
        resp = httpx.post(
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions",
            headers={
                "Authorization": f"Bearer {BAIDU_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "messages": [{"role": "user", "content": prompt}],
                "model": "ernie-4.0-8k"
            },
            timeout=30
        )
        data = resp.json()
        if resp.status_code == 200 and "result" in data:
            return data["result"]
        else:
            return f"百度API异常: {data.get('message', str(data))}"
    except Exception as e:
        return f"百度API错误: {e}"

def call_ali(prompt):
    try:
        resp = httpx.post(
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
            headers={"Authorization": f"Bearer {ALI_API_KEY}"},
            json={
                "model": "qwen-turbo",
                "input": {"prompt": prompt}
            },
            timeout=30
        )
        data = resp.json()
        if resp.status_code == 200 and "output" in data:
            return data["output"]["text"]
        else:
            return f"阿里API异常: {data.get('message', str(data))}"
    except Exception as e:
        return f"阿里API错误: {e}"



def correct_sentence(sentence, lang, native_lang):
    prompt = f"""请检查以下{lang}句子的语法错误，并用{native_lang}解释原因。
句子：{sentence}

请按以下格式返回：
1. 修正后的句子
2. 错误说明（用{native_lang}）
3. 不要使用markdown格式"""
    
    return {
        "doubao": call_doubao(prompt),
        "baidu": call_baidu(prompt),
        "ali": call_ali(prompt)
    }

def generate_slang(topic, lang, native_lang):
    prompt = f"""
请列举1个与{topic}相关的{lang}俚语，附{lang}例句和{native_lang}翻译，不要解释，不要多余内容。不要使用markdown格式。
"""
    return {
        "doubao": call_doubao(prompt),
        "baidu": call_baidu(prompt),
        "ali": call_ali(prompt),
        "web": slang_crawler.crawl_slang(topic, lang, native_lang)
    }


def generate_quiz(lang):
    prompt = f"""
请为{lang}学习者设计4道六级难度的选择题，分别考查：1.词汇 2.语法 3.阅读理解 4.听力理解。每题4个选项，题干和选项要有区分度，答案唯一且准确。听力题请给出一段短音频文本作为题干。请用如下JSON格式返回：
[
  {{"dimension": "词汇", "question": "...", "options": ["A", "B", "C", "D"], "answer": "A"}},
  ...
]
不要有多余解释。
"""
    # 只用豆包模型，提升速度
    quiz_str = call_doubao(prompt)
    import json
    try:
        quiz = json.loads(quiz_str)
        if isinstance(quiz, list):
            return {"questions": [{k: q.get(k) for k in ["dimension","question","options","answer"]} for q in quiz]}
    except:
        pass
    return {"questions": []}

def grade_quiz(lang, level, user_answers_or_payload):
    # 支持quiz_payload（含题目、答案、作答）
    import json
    if isinstance(user_answers_or_payload, dict):
        questions = user_answers_or_payload.get('questions', [])
        user_answers = user_answers_or_payload.get('user_answers', [])
        # 构造题目+正确答案+用户答案的prompt
        q_str = '\n'.join([
            f"{i+1}. {q.get('question','')} 正确答案：{q.get('answer','')}" for i, q in enumerate(questions)
        ])
        a_str = '\n'.join([
            f"{i+1}. {a}" for i, a in enumerate(user_answers)
        ])
        prompt = f"""
你是{lang}老师，请根据以下选择题和学生作答情况进行评分，严格按照如下规则评级：
- 全对为A（雅思难度）
- 错1题为B（六级）
- 错2题为C（四级）
- 错3题为D（高考）
- 全错为E（中考）

题目与正确答案：\n{q_str}

学生作答：\n{a_str}

请只返回等级字母和一句理由。
"""
        result = call_doubao(prompt)
        import re
        match = re.search(r'([ABCDE])', result)
        level = match.group(1) if match else 'E'
        return {
            'level': level,
            'desc': result
        }

def get_exam_by_level(level):
    # ABCDE五级与考试难度映射
    level_map = {
        'A': '雅思',
        'B': '六级',
        'C': '四级',
        'D': '高考',
        'E': '中考',
    }
    return level_map.get(str(level), '雅思')

def generate_vocab(lang, level):
    exam = get_exam_by_level(level)
    prompt = f"""
请为{lang}学习者（{exam}难度，当前等级：{level}）生成10个完全随机词汇，内容和难度要适合该考试，返回JSON数组，如[\"词1\",\"词2\",...]
不要有多余解释。
"""
    vocab_str = call_doubao(prompt)
    import json
    try:
        vocab = json.loads(vocab_str)
        if isinstance(vocab, list):
            return {"vocab": vocab}
    except:
        pass
    return {"vocab": []}

def generate_story(lang, level, vocab):
    exam = get_exam_by_level(level)
    prompt = f"""
请用以下{lang}词汇：{', '.join(vocab)}，为{lang}学习者（{exam}难度，当前等级：{level}）写一个简短小故事，要求用词和语法难度适合该考试和等级。
只返回故事正文，不要解释。
"""
    story = call_doubao(prompt)
    return {"story": story}

def extract_grammar(lang, story):
    prompt = f"""
请从下面这段{lang}小故事中，提取出用到的主要语法点，简要列出，难度和表达要适合当前学习等级。
故事：{story}
只返回语法点列表，不要解释。
"""
    grammar = call_doubao(prompt)
    return {"grammar": grammar} 

def role_chat(lang, role, history):
    # 构造角色prompt
    role_map = {
        '老师': f'你是一名{lang}老师，请用地道、耐心的风格和学生多轮对话，适当引导学习。',
        '同学': f'你是一名{lang}学习者的同学，请用轻松、友好的语气和学生多轮对话。',
        '本地人': f'你是一名{lang}国家的本地人，请用真实、自然的表达和学生多轮对话。',
    }
    system_prompt = role_map.get(role, f'你是{lang}对话者。')
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        messages.append({"role": "user" if msg["role"]=="user" else "assistant", "content": msg["content"]})
    # 只用豆包
    try:
        resp = httpx.post(
            "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
            headers={
                "Authorization": f"Bearer {DOUBAO_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "ep-20250705101727-rxh8s",
                "messages": messages
            },
            timeout=30
        )
        data = resp.json()
        if resp.status_code == 200 and "choices" in data and data["choices"]:
            return {"reply": data["choices"][0]["message"]["content"]}
        else:
            return {"reply": f"豆包API异常: {data.get('error', {}).get('message', str(data))}"}
    except Exception as e:
        return {"reply": f"豆包API错误: {e}"} 