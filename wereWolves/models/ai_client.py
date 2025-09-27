"""
AI客户端统一接口
支持不同大模型的API调用
"""
import json
import requests
from openai import OpenAI
from sparkai.llm.llm import ChatSparkLLM
from sparkai.core.messages import ChatMessage
import websocket
import ssl
import _thread as thread
from urllib.parse import urlparse, urlencode
import base64
import hashlib
import hmac
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time


class AIClient:
    def __init__(self, model_type, config):
        self.model_type = model_type
        self.config = config
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """初始化不同类型的客户端"""
        if self.model_type in ["doubao", "ernie", "qwen", "zhipu"]:
            self.client = OpenAI(
                api_key=self.config["api_key"],
                base_url=self.config["base_url"]
            )
        elif self.model_type == "xunfei":
            self.client = ChatSparkLLM(
                spark_api_url=self.config["url"],
                spark_app_id=self.config["app_id"],
                spark_api_key=self.config["api_key"],
                spark_api_secret=self.config["api_secret"],
                spark_llm_domain=self.config["domain"],
                streaming=False,
            )
    
    async def send_message(self, messages, system_prompt=""):
        """发送消息并获取回复"""
        try:
            if self.model_type == "xunfei":
                return await self._send_xunfei_message(messages, system_prompt)
            else:
                return await self._send_openai_message(messages, system_prompt)
        except Exception as e:
            print(f"模型 {self.model_type} 调用失败: {e}")
            return "抱歉，我现在无法回应。"
    
    async def _send_openai_message(self, messages, system_prompt):
        """使用OpenAI兼容接口发送消息"""
        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        
        for msg in messages:
            formatted_messages.append(msg)
        
        completion = self.client.chat.completions.create(
            model=self.config["model"],
            messages=formatted_messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return completion.choices[0].message.content
    
    async def _send_xunfei_message(self, messages, system_prompt):
        """使用星火认知接口发送消息"""
        # 合并系统提示和用户消息
        content = system_prompt + "\n" + messages[-1]["content"] if system_prompt else messages[-1]["content"]
        
        spark_messages = [ChatMessage(role="user", content=content)]
        response = self.client.generate([spark_messages])
        
        return response.generations[0][0].text