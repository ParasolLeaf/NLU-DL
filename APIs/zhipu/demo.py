from zhipuai import ZhipuAI
import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent.parent / '.env'  # 根据实际路径调整
load_dotenv()

client = ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"))  # 请填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4-plus",  # 请填写您要调用的模型名称
    messages=[
        {"role": "user", "content": "请写一段话介绍北京天坛。"},
    ],
)
print(response)