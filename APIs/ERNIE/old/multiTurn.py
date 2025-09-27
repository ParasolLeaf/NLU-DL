import os
import qianfan
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'  # 根据实际路径调整
load_dotenv()

# 通过环境变量初始化认证信息
# 方式一：【推荐】使用安全认证AK/SK鉴权
# 替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk，如何获取请查看https://cloud.baidu.com/doc/Reference/s/9jwvz2egb
os.environ["QIANFAN_ACCESS_KEY"] = os.getenv("QIANFAN_ACCESS_KEY")
os.environ["QIANFAN_SECRET_KEY"] = os.getenv("QIANFAN_SECRET_KEY")

# 方式二：【不推荐】使用应用AK/SK鉴权
# 替换下列示例中参数，将应用API_Key、应用Secret key值替换为真实值
#os.environ["QIANFAN_AK"] = "应用API_Key"
#os.environ["QIANFAN_SK"] = "应用Secret_Key"

chat_comp = qianfan.ChatCompletion()

# 多轮对话
resp = chat_comp.do(model="ERNIE-Speed-8K", messages=[{
    "role": "user",
    "content": "你好"
},
{
    "role": "assistant",
    "content": "你好，请问有什么我可以帮助你的吗？无论你需要什么帮助，我都会尽力回答你的问题或提供帮助。"
},
{
    "role": "user",
    "content": "北京有哪些美食"
},
])
print(resp["body"])