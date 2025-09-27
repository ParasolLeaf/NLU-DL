# Please install OpenAI SDK first: `pip3 install openai`
from pathlib import Path
from dotenv import load_dotenv
import os
from openai import OpenAI

dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path)

client = OpenAI(api_key=os.getenv("QWEN_API_KEY"),base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "现在的美国总统是谁？"},
    ],
    stream=False
)

print(response.choices[0].message.content)