from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path(__file__).resolve().parent.parent / '.env'  # 根据实际路径调整
load_dotenv()

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # api_key="sk-XXXX",
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "对下面四个数字计算24点（使用所有4个提供的数字，每个数字精确一次，+-/*为24，只需要找到一个解即可）[7 3 8 1]"}]

completion = client.chat.completions.create(
    model="qwen-plus",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    # enable_thinking 参数开启思考过程，QwQ 与 DeepSeek-R1 模型总会进行思考，不支持该参数
    #extra_body={"enable_thinking": True},
    #stream=True,
)
print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")

response = completion.choices[0].message.content
print(response)