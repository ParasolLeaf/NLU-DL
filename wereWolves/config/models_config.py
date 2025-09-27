"""
大模型配置文件
包含各个模型的API配置信息
"""

# 豆包模型配置
DOUBAO_CONFIG = {
    "base_url": "https://ark.cn-beijing.volces.com/api/v3",
    "api_key": "c81b2b6e-6469-4da6-a377-617106aabcb6",  # 请替换为实际的API Key
    "model": "ep-20250917161730-6bf75"
}

# 百度千帆配置
ERNIE_CONFIG = {
    "base_url": "https://qianfan.baidubce.com/v2",
    "api_key": "bce-v3/ALTAK-Etj0lvrkCl7MGkkOTCeWr/805ca0828876600fd02683d34e348b2ed59f7a74",
    "model": "ernie-3.5-8k"
}

# 通义千问配置
QWEN_CONFIG = {
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "api_key": "sk-96a6cc17508541239c40bb84250156d8",
    "model": "qwen-plus"
}

# 智谱AI配置
ZHIPU_CONFIG = {
    "base_url": "https://open.bigmodel.cn/api/paas/v4",
    "api_key": "536e321b77994b12bc33daca8f6982db.a5bfCIV3MEFrVbMi",
    "model": "glm-4-plus"
}

# 星火认知配置
XUNFEI_CONFIG = {
    "app_id": "346f2654",
    "api_key": "08260671f409549445b1bdda8e92f645",
    "api_secret": "MmU3MDcxYjBhNjE2NDYzZDY4NzBmOGJl",
    "url": "wss://spark-api.xf-yun.com/v4.0/chat",
    "domain": "4.0Ultra"
}

# 模型列表（不够8个角色一个模型各一个，使用几个模型的多个实例）
MODELS = [
    {"name": "豆包", "type": "doubao", "config": DOUBAO_CONFIG},
    {"name": "文心一言", "type": "ernie", "config": ERNIE_CONFIG},
    {"name": "文心一言2", "type": "ernie", "config": ERNIE_CONFIG},  # 复用配置
    {"name": "通义千问", "type": "qwen", "config": QWEN_CONFIG},
    {"name": "通义千问2", "type": "qwen", "config": QWEN_CONFIG},   # 复用配置
    {"name": "智谱AI", "type": "zhipu", "config": ZHIPU_CONFIG},
    {"name": "智谱AI2", "type": "zhipu", "config": ZHIPU_CONFIG},   # 复用配置
    {"name": "星火认知", "type": "xunfei", "config": XUNFEI_CONFIG}
]