"""
玩家类定义
每个玩家代表一个AI模型
"""
import asyncio
from models.ai_client import AIClient


class Player:
    def __init__(self, player_id, name, model_type, config, role):
        self.id = player_id
        self.name = name
        self.model_type = model_type
        self.role = role
        self.is_alive = True
        self.ai_client = AIClient(model_type, config)
        self.conversation_history = []
        self.votes_received = 0
        
        # 女巫专用属性
        self.has_antidote = True  # 是否还有解药
        self.has_poison = True    # 是否还有毒药
    
    async def speak(self, prompt, game_state, game_history=None):
        """玩家发言"""
        system_prompt = self._generate_system_prompt(game_state, game_history)
        
        # 构建消息历史
        messages = self.conversation_history.copy()
        messages.append({"role": "user", "content": prompt})
        
        response = await self.ai_client.send_message(messages, system_prompt)
        
        # 更新对话历史
        self.conversation_history.append({"role": "user", "content": prompt})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # 限制历史长度，避免token过多
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return response
    
    def _generate_system_prompt(self, game_state, game_history=None):
        """生成系统提示"""
        base_prompt = f"""你是狼人杀游戏中的{self.role}，编号{self.id}号玩家({self.name})。

游戏规则：
- 狼人：夜晚所有狼人共同选择杀死一名玩家，白天需要隐藏身份
- 村民：白天通过投票找出狼人
- 预言家：夜晚可以查验一名玩家的身份
- 女巫：拥有解药和毒药各一瓶，整局游戏只能各使用一次
- 守卫：夜晚可以守护一名玩家

当前游戏状态：
- 第{game_state['day']}天
- 存活玩家：{', '.join([f"{p.id}号({p.name})" for p in game_state['alive_players']])}
- 已淘汰玩家：{', '.join([f"{p.id}号({p.name})" for p in game_state['dead_players']])}"""

        # 添加游戏历史信息
        if game_history:
            base_prompt += self._format_game_history(game_history)
        
        # 添加角色特定信息
        base_prompt += self._get_role_specific_prompt(game_history)
        
        base_prompt += "\n\n请根据你的角色身份和已知信息进行合理的发言和行动。回复要简洁明了，不要超过150字。"
        
        return base_prompt
    
    def _format_game_history(self, game_history):
        """格式化游戏历史信息"""
        history_text = "\n\n=== 游戏历史信息 ==="
        
        # 添加白天发言历史
        if game_history.get("day_speeches"):
            history_text += "\n\n【历史发言记录】"
            for day, speeches in game_history["day_speeches"].items():
                if day < game_history.get("current_day", 1):  # 只显示之前天数的发言
                    history_text += f"\n第{day}天发言："
                    for speech in speeches:
                        history_text += f"\n  {speech['player_id']}号({speech['name']})：{speech['speech'][:50]}..."
        
        # 添加投票历史
        if game_history.get("voting_history"):
            history_text += "\n\n【投票历史】"
            for day, vote_info in game_history["voting_history"].items():
                eliminated = vote_info["eliminated"]
                if eliminated["player_id"]:
                    history_text += f"\n第{day}天：{eliminated['player_id']}号({eliminated['name']})被投票淘汰，身份是{eliminated['role']}"
                else:
                    history_text += f"\n第{day}天：无人被淘汰"
        
        # 添加夜晚结果
        if game_history.get("night_results"):
            history_text += "\n\n【夜晚结果】"
            for day, result in game_history["night_results"].items():
                if result["deaths"]:
                    death_info = ", ".join([f"{d['player_id']}号({d['name']})" for d in result["deaths"]])
                    history_text += f"\n第{day}晚：{death_info}死亡"
                else:
                    history_text += f"\n第{day}晚：平安夜"
        
        return history_text
    
    def _get_role_specific_prompt(self, game_history):
        """获取角色特定的提示信息"""
        role_prompt = ""
        
        if self.role == "狼人":
            role_prompt += "\n\n【你的身份：狼人】"
            role_prompt += "\n- 你需要隐藏狼人身份，白天要装作村民"
            role_prompt += "\n- 夜晚与其他狼人商议杀人目标，每晚所有狼人只能共同杀死一名玩家"
            
            if game_history and "role_specific_info" in game_history:
                role_info = game_history["role_specific_info"]
                if "werewolf_teammates" in role_info:
                    teammates = ", ".join([f"{t['player_id']}号({t['name']})" for t in role_info["werewolf_teammates"]])
                    role_prompt += f"\n- 你的狼人队友：{teammates}"
                
                if "werewolf_kills" in role_info:
                    role_prompt += "\n- 狼人团队的杀人记录："
                    for day, kill_info in role_info["werewolf_kills"].items():
                        if kill_info["target_id"]:
                            role_prompt += f"\n  第{day}晚杀死了{kill_info['target_id']}号({kill_info['target_name']})"
        
        elif self.role == "预言家":
            role_prompt += "\n\n【你的身份：预言家】"
            role_prompt += "\n- 你可以在夜晚查验玩家身份，白天可以透露信息帮助村民找出狼人"
            
            if game_history and "role_specific_info" in game_history:
                role_info = game_history["role_specific_info"]
                if "seer_results" in role_info:
                    role_prompt += "\n- 你的查验结果："
                    for day, result in role_info["seer_results"].items():
                        role_prompt += f"\n  第{day}晚查验{result['target_id']}号({result['target_name']})：{result['result']}"
        
        elif self.role == "女巫":
            antidote_status = "已使用" if not self.has_antidote else "可用"
            poison_status = "已使用" if not self.has_poison else "可用"
            role_prompt += "\n\n【你的身份：女巫】"
            role_prompt += f"\n- 你有解药({antidote_status})和毒药({poison_status})，整局游戏各只能使用一次"
            role_prompt += "\n- 解药可以救活被杀的人，毒药可以毒死一个人"
            
            if game_history and "role_specific_info" in game_history:
                role_info = game_history["role_specific_info"]
                if "potion_usage" in role_info and "usage_history" in role_info["potion_usage"]:
                    role_prompt += "\n- 你的药品使用记录："
                    for day, usage in role_info["potion_usage"]["usage_history"].items():
                        if "saved" in usage:
                            saved = usage["saved"]
                            role_prompt += f"\n  第{day}晚使用解药救了{saved['target_id']}号({saved['target_name']})"
                        if "poisoned" in usage:
                            poisoned = usage["poisoned"]
                            role_prompt += f"\n  第{day}晚使用毒药毒死了{poisoned['target_id']}号({poisoned['target_name']})"
        
        elif self.role == "守卫":
            role_prompt += "\n\n【你的身份：守卫】"
            role_prompt += "\n- 你可以在夜晚守护一名玩家，被守护的玩家当晚不会死亡"
            
            if game_history and "role_specific_info" in game_history:
                role_info = game_history["role_specific_info"]
                if "guard_history" in role_info:
                    role_prompt += "\n- 你的守护记录："
                    for day, guard_info in role_info["guard_history"].items():
                        role_prompt += f"\n  第{day}晚守护了{guard_info['target_id']}号({guard_info['target_name']})"
        
        elif self.role == "村民":
            role_prompt += "\n\n【你的身份：村民】"
            role_prompt += "\n- 你是普通村民，白天通过投票找出狼人"
            role_prompt += "\n- 仔细观察其他玩家的发言，寻找狼人的破绽"
        
        return role_prompt
    
    def die(self):
        """玩家死亡"""
        self.is_alive = False
    
    def reset_votes(self):
        """重置投票数"""
        self.votes_received = 0
    
    def use_antidote(self):
        """使用解药"""
        if self.has_antidote:
            self.has_antidote = False
            return True
        return False
    
    def use_poison(self):
        """使用毒药"""
        if self.has_poison:
            self.has_poison = False
            return True
        return False