from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from modules.travel_service import generate_travel_plan
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="travel_api.log",
)
logger = logging.getLogger("travel_api")

app = FastAPI(
    title="旅行规划API",
    description="智能旅行计划生成服务",
    version="1.0"
)


class TravelRequest(BaseModel):
    destination: str
    duration: int
    interests: str
    budget: str
    start_date: str
    use_attractions: bool = False
    attraction_num: int = 5


@app.post("/generate-plan")
async def create_travel_plan(request: TravelRequest):
    try:
        logger.info(f"收到请求: {request.destination}, {request.duration}天, 出发日期: {request.start_date}")

        # 生成旅行计划
        plan = await generate_travel_plan(
            destination=request.destination,
            duration=request.duration,
            interests=request.interests,
            budget=request.budget,
            start_date=request.start_date
        )

        return {"plan": plan}

    except Exception as e:
        logger.exception("生成旅行计划失败")
        raise HTTPException(500, "旅行计划生成失败") from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
