from baidusearch.baidusearch import search
import requests
from bs4 import BeautifulSoup
import time
import random
import os
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path)

client = OpenAI(api_key=os.getenv("QWEN_API_KEY"), base_url="https://api.deepseek.com")
client = OpenAI(api_key=os.getenv("QWEN_API_KEY"),base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

results = search('现任美国总统是谁？') 
print(results)


response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": str(results)},
        {"role": "user", "content": "参考上面信息回答：现任美国总统（2025年6月）是谁？"},
    ],
    stream=False
)

print(response.choices[0].message.content)
