import base64
from zhipuai import ZhipuAI
import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent.parent / '.env'  # 根据实际路径调整
load_dotenv()

img_path = "./img/disney.jpg"
with open(img_path, 'rb') as img_file:
    img_base = base64.b64encode(img_file.read()).decode('utf-8')

client = ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY")) # 填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4v-plus-0111",  # 填写需要调用的模型名称
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "image_url",
            "image_url": {
                "url": img_base
                # "url": "https://img1.baidu.com/it/u=1369931113,3388870256&fm=253&app=138&size=w931&n=0&f=JPEG&fmt=auto?sec=1703696400&t=f3028c7a1dca43a080aeb8239f09cc2f"
            }
          },
          {
            "type": "text",
            "text": "请描述上述图片"
          }
        ]
      }
    ]
)
print(response.choices[0].message)