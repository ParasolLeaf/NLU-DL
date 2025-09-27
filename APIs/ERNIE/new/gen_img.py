import requests
import json
import os
from urllib.parse import urlparse
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'  # 根据实际路径调整
load_dotenv()
auth_token = os.getenv("ERNIE_NEW_API_KEY")

# 从URL下载图片到本地
def download_image(image_url, save_path=None):
    try:
        # 发送GET请求下载图片
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        
        # 如果没有指定保存路径，自动生成文件名
        if save_path is None:
            # 从URL中提取文件名，或使用默认名称
            parsed_url = urlparse(image_url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                filename = "generated_image.png"
            save_path = filename
        
        # 确保保存目录存在
        save_dir = os.path.dirname(save_path)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # 写入文件
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"图片已保存到: {save_path}")
        return save_path
        
    except Exception as e:
        print(f"下载图片失败: {e}")
        return None

# 解析API响应并下载所有图片
def parse_and_download_images(response_text):
    try:
        result = json.loads(response_text)
        if 'data' in result and len(result['data']) > 0:
            downloaded_files = []
            for i, item in enumerate(result['data']):
                if 'url' in item:
                    image_url = item['url']
                    # 下载图片并记录保存路径
                    saved_path = download_image(image_url, f"generated_image_{i+1}.png")
                    if saved_path:
                        downloaded_files.append(saved_path)
            return downloaded_files
        else:
            print("响应中没有找到图片数据")
            return []
    except json.JSONDecodeError:
        print("响应不是有效的JSON格式")
        return []
    except Exception as e:
        print(f"处理响应时出错: {e}")
        return []

def main():
    url = "https://qianfan.baidubce.com/v2/images/generations"
    
    payload = json.dumps({
    "model": "irag-1.0",
    "prompt": "画一只带着蝴蝶结的小狗"
  })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {auth_token}"
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    
    # 调用解析并下载函数
    downloaded_files = parse_and_download_images(response.text)
    if downloaded_files:
        print(f"成功下载了 {len(downloaded_files)} 张图片")
    

if __name__ == '__main__':
    main()