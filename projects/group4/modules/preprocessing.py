import re
import logging
import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="preprocessing.log",
)

logger = logging.getLogger("input_cleaner")


def validate_date(date_str: str) -> bool:
    """验证日期格式是否为YYYY-MM-DD"""
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def clean_input(text: str, is_date: bool = False) -> str:
    """清理用户输入"""
    if is_date and validate_date(text):
        return text

    if not text or not isinstance(text, str):
        return ""

    try:
        # 1. 移除潜在危险字符
        clean_text = re.sub(r"[<>{}|\\^~\[\]]", "", text)

        # 2. 标准化空格
        clean_text = re.sub(r"\s+", " ", clean_text).strip()

        # 3. 截断过长的输入
        if len(clean_text) > 500:
            clean_text = clean_text[:500]
            logger.warning(f"输入过长被截断")

        return clean_text

    except Exception as e:
        logger.error(f"输入清理失败: {str(e)}")
        return text
