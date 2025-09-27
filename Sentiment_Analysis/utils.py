import matplotlib.pyplot as plt
from collections import Counter


def setup_matplotlib():
    """配置matplotlib的中文显示"""
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False


def create_visualization(sentiment_counts, output_file):
    """创建并保存可视化结果"""
    # 只保留积极、消极、中立的统计
    valid_sentiments = {k: v for k, v in sentiment_counts.items()
                        if k in ['积极', '消极', '中立']}

    # 设置颜色映射
    colors = {
        '积极': '#2ecc71',  # 绿色
        '中立': '#f1c40f',  # 黄色
        '消极': '#e74c3c'  # 红色
    }

    plt.figure(figsize=(10, 6))
    bars = plt.bar(valid_sentiments.keys(),
                   valid_sentiments.values(),
                   color=[colors[k] for k in valid_sentiments.keys()])

    plt.title('评论情感分析结果', fontsize=14, pad=15)
    plt.xlabel('情感倾向', fontsize=12)
    plt.ylabel('评论数量', fontsize=12)

    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{int(height)}',
                 ha='center', va='bottom')

    # 优化图表样式
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()


def print_statistics(sentiment_counts):
    """打印统计结果"""
    print("\n情感分析统计结果:")
    valid_sentiments = ['积极', '消极', '中立']
    for sentiment in valid_sentiments:
        count = sentiment_counts.get(sentiment, 0)
        print(f"{sentiment}: {count}条")