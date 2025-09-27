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

client = OpenAI(api_key=os.getenv("QWEN_API_KEY"),base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

question = '现在（2025年6月）的美国总统是谁？'

response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": question},
    ],
    stream=False
)
response = response.choices[0].message.content
print('###############################')
print(response)

new_response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": question},
        {"role": "assistant", "content": response},
        {"role": "user", "content": "现在，你可以使用一次从网页上搜索的功能，以查找最新的新闻。请根据你的问题和答案，判断你的回答是否需要这一功能来进一步完善。"},
    ],
    stream=False
)
new_response = new_response.choices[0].message.content
print('###############################')
print(new_response)

search_response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": question},
        {"role": "assistant", "content": response},
        {"role": "user", "content": "现在，你可以使用一次从网页上搜索的功能，以查找最新的新闻。请根据你的问题和答案，判断你的回答是否需要这一功能来进一步完善。"},
        {"role": "assistant", "content": new_response},
        {"role": "user", "content": "根据上述回答，总结是否需要搜索。请用“搜索：（搜索内容）”或“不搜索”回答。"},
    ],
    stream=False
)
search_response = search_response.choices[0].message.content
print('###############################')
print(search_response)

if '搜索：' in search_response:
    search_response = search_response[3:]
    print(search_response)
    results = search(search_response) 
    print('###############################')
    print(results)
    
    
    final_response = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "user", "content": str(results)},
            {"role": "user", "content": "参考上面信息回答：现任美国总统是谁？"},
        ],
        stream=False
    )
    final_response= final_response.choices[0].message.content
    print('###############################')
    print(final_response)
else:
    print('###############################')
    print(response)
