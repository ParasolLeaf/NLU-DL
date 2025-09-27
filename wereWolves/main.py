"""
狼人杀游戏主程序
"""
import asyncio
from models.player import Player
from game.werewolf_game import WerewolfGame
from config.models_config import MODELS


async def main():
    print("初始化8人狼人杀游戏...")
    
    # 创建8个玩家，每个使用不同的AI模型
    players = []
    for i, model_info in enumerate(MODELS):
        player = Player(
            player_id=i + 1,
            name=model_info["name"],
            model_type=model_info["type"],
            config=model_info["config"],
            role=""  # 角色将在游戏开始时分配
        )
        players.append(player)
    
    # 创建并开始游戏
    game = WerewolfGame(players)
    await game.run_game()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n游戏被用户中断")
    except Exception as e:
        print(f"\n游戏运行出错: {e}")