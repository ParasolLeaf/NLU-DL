import requests
import json
import base64
import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'  # 根据实际路径调整
load_dotenv()
auth_token = os.getenv("ERNIE_NEW_API_KEY")

# 将本地图片文件编码为base64格式的data URL
def encode_local_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在: {image_path}")
    
    # 获取文件扩展名来确定MIME类型
    file_extension = os.path.splitext(image_path)[1].lower()
    mime_type_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg', 
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.webp': 'image/webp'
    }
    
    mime_type = mime_type_map.get(file_extension, 'image/jpeg')
    
    # 读取并编码图片文件
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    return f"data:{mime_type};base64,{encoded_string}"


def main():
    url = "https://qianfan.baidubce.com/v2/chat/completions"

    # 示例：使用本地图片（将路径替换为你的实际图片路径）
    local_image_url = encode_local_image("/bus/home/wuyt/DL-NLU/ERNIE/img/street.jpg")

    payload = json.dumps({
        "model": "ernie-4.5-vl-28b-a3b",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "分别使用1句话描述以下图片的内容"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": local_image_url # 若为本地图片需要进行base64编码
                            # "url": "https://img95.699pic.com/photo/50050/5334.jpg_wh860.jpg" # 若为在线图片直接填入图片url链接即可
                        }
                    }
                ]
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {auth_token}"
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    main()