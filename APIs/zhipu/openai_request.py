from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent.parent / '.env'  # 根据实际路径调整
load_dotenv()

client = OpenAI(
  base_url = 'https://open.bigmodel.cn/api/paas/v4',
  api_key  = os.getenv("ZHIPU_API_KEY")
)

completion = client.chat.completions.create(
  model='glm-4v-plus-0111',
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
              "url": "https://img1.baidu.com/it/u=1369931113,3388870256&fm=253&app=138&size=w931&n=0&f=JPEG&fmt=auto?sec=1703696400&t=f3028c7a1dca43a080aeb8239f09cc2f"
          }
        },
        {
          "type": "text",
          "text": "请描述这个图片，并推测图中可能拍摄地点。"
        }
      ]
    }
  ], 
) 

print(completion)    
