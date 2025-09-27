import qianfan
import pandas as pd


class SentimentAnalyzer:
    def __init__(self, model_name):
        self.model_name = model_name
        self.chat_comp = qianfan.ChatCompletion()

    def analyze(self, text):
        """分析单条评论的情感"""
        prompt = f"""
        请分析以下评论的情感倾向，只需回复：积极/消极/中立
        评论：{text}
        """

        try:
            response = self.chat_comp.do(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            # 清理结果文本：去除空白字符和标点符号
            result = response["body"]["result"].strip().rstrip('。.，,')

            # 标准化结果
            sentiment_mapping = {
                '积极': '积极',
                '正面': '积极',
                '好评': '积极',
                '消极': '消极',
                '负面': '消极',
                '差评': '消极',
                '中立': '中立',
                '一般': '中立',
                '普通': '中立'
            }

            # 查找匹配的情感类别
            result = sentiment_mapping.get(result, '中立')
            return result

        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return "中立"

    def analyze_batch(self, comments, callback=None):
        """批量分析评论"""
        sentiments = []
        for i, comment in enumerate(comments, 1):
            if pd.isna(comment):
                continue
            sentiment = self.analyze(str(comment))
            sentiments.append(sentiment)

            if callback:
                callback(i, len(comments), comment, sentiment)

        return sentiments