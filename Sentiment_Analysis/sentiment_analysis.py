import os
import pandas as pd
from config import *
from utils import setup_matplotlib, create_visualization, print_statistics
from sentiment_analyzer import SentimentAnalyzer
from collections import Counter


def progress_callback(current, total, comment, sentiment):
    """进度回调函数"""
    print(f"进度: {current}/{total}")
    print(f"评论: {comment}")
    print(f"情感: {sentiment}\n")


def main():
    # 设置环境变量
    os.environ["QIANFAN_ACCESS_KEY"] = QIANFAN_ACCESS_KEY
    os.environ["QIANFAN_SECRET_KEY"] = QIANFAN_SECRET_KEY

    # 设置matplotlib
    setup_matplotlib()

    try:
        # 尝试不同的编码方式读取CSV文件
        encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030']
        df = None

        for encoding in encodings:
            try:
                df = pd.read_csv(INPUT_CSV, encoding=encoding)
                print(f"成功使用 {encoding} 编码读取文件")
                break
            except UnicodeDecodeError:
                continue

        if df is None:
            raise Exception("无法使用已知编码格式读取文件")

        comments = df['review'].tolist()
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # 初始化情感分析器
    analyzer = SentimentAnalyzer(MODEL_NAME)

    # 进行情感分析
    print("开始分析评论...")
    sentiments = analyzer.analyze_batch(comments, progress_callback)

    # 统计结果
    sentiment_counts = Counter(sentiments)

    # 创建可视化
    create_visualization(sentiment_counts, OUTPUT_PLOT)

    # 打印统计结果
    print_statistics(sentiment_counts)

    # 保存结果到CSV
    results_df = pd.DataFrame({
        'review': comments,
        'sentiment': sentiments
    })
    results_df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
    print(f"\n分析结果已保存到 {OUTPUT_CSV}")


if __name__ == "__main__":
    main()