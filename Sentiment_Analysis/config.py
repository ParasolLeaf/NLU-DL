import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent / '.env'  # 根据实际路径调整
load_dotenv()

# ERNIE API配置
QIANFAN_ACCESS_KEY = os.getenv("QIANFAN_ACCESS_KEY")
QIANFAN_SECRET_KEY = os.getenv("QIANFAN_SECRET_KEY")

# 文件路径配置
# INPUT_CSV = './data/ChnSentiCorp_htl_all.csv'
INPUT_CSV = './data/ChnSentiCorp_htl_short.csv'
OUTPUT_CSV = './output/1sentiment_analysis_results.csv'
OUTPUT_PLOT = './output/1sentiment_analysis_results.png'

# 模型配置
MODEL_NAME = "ERNIE-Speed-128K"