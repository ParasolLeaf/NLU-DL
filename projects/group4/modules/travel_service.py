from .qwen_integration import get_qwen_completion
from .preprocessing import clean_input
from .draft_weather import search_baidu_and_scrape_with_playwright
from .draft_tour import search_for_destination
import logging

logger = logging.getLogger("travel_service")


async def generate_travel_plan(
        destination: str,
        duration: int,
        interests: str,
        budget: str,
        start_date: str,
        use_attractions: bool = False,
        attraction_num: int = 5
) -> str:
    """生成旅行计划的核心逻辑"""
    try:
        # 清理输入
        clean_dest = clean_input(destination)
        clean_interests = clean_input(interests)

        # 获取天气数据
        web_data_weather = await search_baidu_and_scrape_with_playwright(f"{clean_dest}天气")

        # 如果启用了景点搜索
        attractions_info = ""
        if use_attractions:
            try:
                attractions_info = await search_for_destination(clean_dest, attraction_num)
                logger.info(f"获取到 {attraction_num} 个景点信息")
            except Exception as e:
                logger.error(f"景点搜索失败: {str(e)}")
                attractions_info = f"景点搜索失败: {str(e)}"

        # 构建提示词
        weather_tip = '若用户的旅行时长在给出的天气信息的时间范围内，则根据天气信息辅助计划，若超出旅行时长则根据日期判断季节预估天气信息辅助计划。根据天气情况结合景点是室内或室外'\
                      '活动的信息，尽可能将室外活动放到不下雨或天气相对较好的日期中，如晴天优于阴天优于下雨。若用户旅行时长中不下雨的时间结合景点游玩时间不足以满足全部户外活动都在不下雨的天数，则需要提醒用户带伞。 '
        prompt = f"""
        你是一个专业的旅行规划师，请为{start_date}出发的游客创建一份{duration}天的{clean_dest}旅行计划。
        游客兴趣：{clean_interests}
        预算范围：{budget}
        当前旅行建议（天气情况，请务必考虑）：{web_data_weather}
        {weather_tip}
        用户较为想去的景点信息：{attractions_info if use_attractions else ""}

        请按以下格式规划：
        1. 实用贴士（交通、天气、节日活动等）
        2. 每日行程安排（上午、下午、晚上）
        3. 推荐景点和活动
        4. 餐饮建议
        5. 住宿推荐
        6. 预算分配建议
        7. 出发前准备建议（签证、疫苗等）
        
        重点应放在每日行程安排中，使用最长的篇幅
        如有天气信息在每日行程安排时标注天气及温度
        """

        # 调用模型生成计划
        plan = await get_qwen_completion(prompt=prompt, max_tokens=3000)
        return plan

    except Exception as e:
        logger.error(f"生成旅行计划失败: {str(e)}")
        raise
