import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'  # 根据实际路径调整
load_dotenv()
auth_token = os.getenv("ERNIE_NEW_API_KEY")

def main():
    url = "https://qianfan.baidubce.com/v2/chat/completions"
    
    payload = json.dumps({
        "model": "ernie-3.5-8k",
        "messages": [
            {
                "role": "system",
                "content": "平台助手"
            },
            {
                "role": "user",
                "content": "请用一段话介绍北京烤鸭。"
            }
        ]
    })

    # 将api页面获得的bce开头的秘钥粘贴至下述Bearer之后
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {auth_token}"
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    

if __name__ == '__main__':
    main()