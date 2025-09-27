import os
import httpx
import logging
from dotenv import load_dotenv

logger = logging.getLogger("api_integration")

load_dotenv()

QWEN_API_BASE = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
QWEN_API_KEY = os.getenv("QWEN_API_KEY")


async def get_qwen_completion(prompt: str, temperature: float = 0.7, max_tokens: int = 800) -> str:
    """获取Qwen模型补全"""
    if not QWEN_API_KEY:
        logger.error("Qwen API Key未配置")
        return "错误：API密钥未配置"

    url = QWEN_API_BASE
    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "qwen-turbo",
        "input": {"messages": [{"role": "user", "content": prompt}]},
        "parameters": {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "result_format": "text"
        }
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            if "output" in data and "text" in data["output"]:
                return data["output"]["text"]
            else:
                logger.error(f"无法解析Qwen响应: {data}")
                return "错误：无法解析API响应"

    except Exception as e:
        logger.exception("Qwen API调用失败")
        return f"错误：{str(e)}"
