import pandas as pd

def get_user_stats(user_id):
    # 假设有用户纠错历史数据csv
    try:
        df = pd.read_csv(f"data/{user_id}_errors.csv")
        stats = df['error_type'].value_counts().to_dict()
        return {"stats": stats}
    except Exception as e:
        return {"error": str(e)} 