import gradio as gr
import requests
import logging
import datetime

# 配置API端点
API_URL = "http://localhost:8000/generate-plan"

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="travel_gui.log",
)
logger = logging.getLogger("travel_planner_gui")


def validate_date(date_str: str) -> bool:
    """验证日期格式是否为YYYY-MM-DD"""
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def generate_travel_plan(destination, duration, interests, budget, start_date, use_attractions, attraction_num):
    """发送旅行计划请求"""
    # 验证日期格式
    if not validate_date(start_date):
        return "错误：日期格式不正确，请使用 YYYY-MM-DD 格式"

    logger.info(f"生成计划: {destination}, {duration}天, 兴趣: {interests}, 预算: {budget}, 出发日期: {start_date}")
    logger.info(f"景点搜索: {'启用' if use_attractions else '禁用'}, 数量: {attraction_num}")

    try:
        # 构建请求
        request_data = {
            "destination": destination,
            "duration": duration,
            "interests": interests,
            "budget": budget,
            "start_date": start_date
        }

        # 如果启用了景点搜索，添加相关参数
        if use_attractions:
            request_data["use_attractions"] = True
            request_data["attraction_num"] = int(attraction_num)

        response = requests.post(
            API_URL,
            json=request_data,
            timeout=240
        )

        # 检查响应状态
        if response.status_code != 200:
            error_msg = f"API错误: {response.status_code} - {response.text[:200]}"
            logger.error(error_msg)
            return error_msg

        logger.info("成功收到旅行计划")
        plan = response.json()["plan"]
        return plan

    except Exception as e:
        error = f"请求失败: {str(e)}"
        logger.exception(error)
        return error


# 创建Gradio界面
with gr.Blocks(
        title="智能旅行规划师",
        theme=gr.themes.Soft(),
        css="""
    .output-box {
        font-family: 'Microsoft YaHei', 'PingFang SC', 'SimHei', sans-serif;
        font-size: 16px;
        line-height: 1.6;
        white-space: pre-wrap;
        border-radius: 8px;
        padding: 20px;
        min-height: 300px;
        background-color: #1F2937;
        color: white;
    }

    .input-box {
        font-size: 16px;
        padding: 12px;
    }
    .date-hint {
        font-size: 12px;
        color: #666;
        margin-top: 4px;
    }
    .optional-section {
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px dashed #ddd;
    }
    """
) as demo:
    gr.Markdown("# ✈️ 智能旅行规划师")
    gr.Markdown("为您量身定制完美旅行计划")

    today = datetime.date.today().strftime("%Y-%m-%d")

    # 输入区域
    with gr.Row():
        with gr.Column(scale=1):
            destination = gr.Textbox(
                label="旅行目的地",
                placeholder="例如：北京、巴黎、东京...",
                elem_classes=["input-box"]
            )
            duration = gr.Slider(
                1, 10, value=5, step=1,
                label="旅行天数",
                info="选择您的旅行时长"
            )
            interests = gr.Textbox(
                label="兴趣偏好",
                placeholder="例如：美食、历史、购物、自然风光...",
                lines=2,
                elem_classes=["input-box"]
            )
            budget = gr.Dropdown(
                ["经济型", "舒适型", "豪华型"],
                value="舒适型",
                label="预算范围"
            )
            start_date = gr.Textbox(
                label="出发日期",
                value=today,
                placeholder="格式：YYYY-MM-DD",
                elem_classes=["input-box"]
            )
            gr.Markdown("示例：2023-08-15", elem_classes=["date-hint"])

            # 新增景点搜索选项
            with gr.Group(elem_classes=["optional-section"]):
                use_attractions = gr.Checkbox(
                    label="启用景点搜索功能",
                    value=False,
                    info="启用后将从网络搜索精选景点"
                )
                attraction_num = gr.Slider(
                    1, 20, value=5, step=1,
                    label="景点数量",
                    info="（建议5~10个）",
                    visible=False
                )

            submit_btn = gr.Button("生成旅行计划", variant="primary")

        # 输出区域
        with gr.Column(scale=2):
            output_area = gr.Markdown(
                value="<span span style='color: white; font-size: 36px;'>您的专属旅行计划</span>",
                max_height=700,
                show_copy_button=True,
                elem_classes=["output-box"]
            )

    # 添加交互：当景点搜索开关变化时显示/隐藏景点数量滑块
    use_attractions.change(
        fn=lambda x: gr.Slider(visible=x),
        inputs=use_attractions,
        outputs=attraction_num
    )

    # 连接交互
    submit_btn.click(
        fn=generate_travel_plan,
        inputs=[destination, duration, interests, budget, start_date, use_attractions, attraction_num],
        outputs=output_area
    )

# 启动界面
if __name__ == "__main__":
    # 添加详细的启动日志
    logging.info("正在启动Gradio服务...")
    print(f"请访问 http://localhost:7860 以启动")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        share=False,
        debug=True
    )
    logging.info(f"服务已在 http://0.0.0.0:7860 启动")
