# 8人狼人杀大模型对战游戏

这是一个让8个不同的大模型AI作为玩家进行狼人杀游戏的Python项目。

## 功能特点

- 支持多种大模型：豆包、文心一言、通义千问、智谱AI、星火认知
- 完整的狼人杀角色：狼人、村民、预言家、女巫、守卫
- 完整的游戏流程：白天发言、投票、夜晚行动
- 彩色终端输出，实时显示游戏进程
- 详细的游戏状态和统计信息

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置API密钥

在 `config/models_config.py` 文件中配置各个模型的API密钥：

```python
# 示例配置
DOUBAO_CONFIG = {
    "base_url": "https://ark.cn-beijing.volces.com/api/v3",
    "api_key": "your_ark_api_key",  # 替换为你的API Key
    "model": "ep-20250630094217-cmzft"
}
```

## 运行游戏

```bash
python main.py
```

## 游戏规则

### 角色分配（8人局）
- 狼人 x3：夜晚共同选择杀死一名玩家，白天隐藏身份
- 预言家 x1：夜晚查验身份
- 女巫 x1：拥有解药和毒药各一瓶
- 守卫 x1：夜晚守护一名玩家
- 村民 x2：通过投票找出狼人

### 游戏流程
1. 白天阶段：所有玩家自由发言讨论
2. 投票阶段：投票淘汰一名玩家
3. 夜晚阶段：特殊角色执行技能
   - 狼人团队共同选择杀死一名玩家
   - 预言家查验
   - 女巫救人/毒人
   - 守卫守护

### 胜利条件
- 狼人胜利：狼人数量 ≥ 好人数量
- 村民胜利：所有狼人被淘汰

## 项目结构

```
├── config/
│   └── models_config.py    # 模型配置
├── models/
│   ├── ai_client.py        # AI客户端统一接口
│   └── player.py           # 玩家类
├── game/
│   ├── game_state.py       # 游戏状态管理
│   └── werewolf_game.py    # 游戏主逻辑
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖包
└── README.md              # 说明文档
```

## 注意事项

1. 确保所有API密钥都已正确配置
2. 某些模型可能有调用频率限制，游戏中已添加适当延迟
3. 如果某个模型调用失败，会显示错误信息并继续游戏
4. 游戏支持键盘中断（Ctrl+C）退出

## 自定义扩展

- 可以在 `config/models_config.py` 中添加更多模型
- 可以修改 `game/werewolf_game.py` 中的角色分配和游戏规则
- 可以调整AI的系统提示词来改变游戏风格
