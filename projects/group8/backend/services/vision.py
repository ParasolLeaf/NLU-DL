import httpx

DOUBAO_API_KEY = ""  # 需要更新
BAIDU_API_KEY = "bce-XXX"  # 需要更新
ALI_API_KEY = "sk-XXX"

def doubao_vision(image_urls, prompt="图片主要讲了什么?"):
    try:
        # 构造 messages content
        content = [{"type": "text", "text": prompt}]
        for url in image_urls:
            content.append({"type": "image_url", "image_url": {"url": url}})
        resp = httpx.post(
            "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
            headers={
                "Authorization": f"Bearer {DOUBAO_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "doubao-1.5-vision-lite-250315",
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            },
            timeout=30
        )
        data = resp.json()
        # 豆包返回格式需根据实际API调整
        if resp.status_code == 200 and "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        else:
            return f"豆包视觉API异常: {data}"
    except Exception as e:
        return f"豆包视觉API错误: {e}"

def baidu_vision(image_urls, prompt="请用一句话描述图片内容"):
    try:
        content = [{"type": "text", "text": prompt}]
        for url in image_urls:
            content.append({"type": "image_url", "image_url": {"url": url}})
        resp = httpx.post(
            "https://qianfan.baidubce.com/v2/chat/completions",
            headers={
                "Authorization": f"Bearer {BAIDU_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-vl2",
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            },
            timeout=30
        )
        data = resp.json()
        # 百度返回格式需根据实际API调整
        if resp.status_code == 200 and "result" in data:
            return data["result"]
        elif "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        else:
            return f"百度视觉API异常: {data}"
    except Exception as e:
        return f"百度视觉API错误: {e}"

def ali_vision(image_urls, prompt="请用一句话描述图片内容"):
    try:
        content = []
        for url in image_urls:
            content.append({"type": "image_url", "image_url": {"url": url}})
        content.append({"type": "text", "text": prompt})
        resp = httpx.post(
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {ALI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "qwen-vl-plus",  # 官方文档推荐视觉模型
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            },
            timeout=30
        )
        data = resp.json()
        if resp.status_code == 200 and "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        else:
            return f"阿里视觉API异常: {data}"
    except Exception as e:
        return f"阿里视觉API错误: {e}"

def describe(image_urls, prompt="请用一句话描述图片内容"):
    return {
        "doubao": doubao_vision(image_urls, prompt),
        "baidu": baidu_vision(image_urls, prompt),
        "ali": ali_vision(image_urls, prompt)
    }