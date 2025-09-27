from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import os

dotenv_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'  # 根据实际路径调整
load_dotenv()

client = OpenAI(
    # api_key="bce-xxx",
    api_key= os.getenv("ERNIE_NEW_API_KEY"),
    base_url="https://qianfan.baidubce.com/v2",
)

completion = client.chat.completions.create(
    model="ernie-3.5-8k",
    messages=[{'role': 'user', 'content': '请用一段话介绍北京烤鸭。'}]
)

print(completion.choices[0].message.content)
