"""
游戏状态管理
"""
import random
from collections import Counter


class GameState:
    def __init__(self, players):
        self.players = players
        self.alive_players = players.copy()
        self.dead_players = []
        self.day = 1
        self.phase = "day"  # day, night, voting
        self.votes = {}
        self.night_actions = {}
        self.game_over = False
        self.winner = None
        
        # 游戏历史记录
        self.day_speeches = {}  # 每天的发言记录 {day: [{player_id, name, speech}]}
        self.voting_history = {}  # 投票历史 {day: {voter_id: target_id, result: eliminated_player}}
        self.night_results = {}  # 夜晚结果 {day: {deaths: [], actions: {}}}
        self.seer_results = {}  # 预言家查验结果 {day: {target_id: result}}
        
        # 角色统计
        self.werewolves = [p for p in players if p.role == "狼人"]
        self.villagers = [p for p in players if p.role in ["村民", "预言家", "女巫", "守卫"]]
    
    def add_day_speech(self, player, speech):
        """添加白天发言记录"""
        if self.day not in self.day_speeches:
            self.day_speeches[self.day] = []
        
        self.day_speeches[self.day].append({
            "player_id": player.id,
            "name": player.name,
            "speech": speech
        })
    
    def add_voting_record(self, eliminated_player):
        """添加投票记录"""
        self.voting_history[self.day] = {
            "votes": self.votes.copy(),
            "eliminated": {
                "player_id": eliminated_player.id if eliminated_player else None,
                "name": eliminated_player.name if eliminated_player else None,
                "role": eliminated_player.role if eliminated_player else None
            }
        }
    
    def add_night_result(self, deaths, actions):
        """添加夜晚结果记录"""
        self.night_results[self.day] = {
            "deaths": [{"player_id": p.id, "name": p.name, "role": p.role} for p in deaths],
            "actions": actions.copy()
        }
    
    def add_seer_result(self, target_player, result):
        """添加预言家查验结果"""
        if self.day not in self.seer_results:
            self.seer_results[self.day] = {}
        
        self.seer_results[self.day] = {
            "target_id": target_player.id,
            "target_name": target_player.name,
            "result": result
        }
    
    def get_game_history_for_player(self, player):
        """获取特定玩家的游戏历史信息"""
        history = {
            "day_speeches": self.day_speeches.copy(),
            "voting_history": self.voting_history.copy(),
            "night_results": self.night_results.copy(),
            "role_specific_info": self._get_role_specific_info(player)
        }
        return history
    
    def _get_role_specific_info(self, player):
        """获取角色特定的信息"""
        role_info = {}
        
        if player.role == "预言家":
            # 预言家可以知道自己的所有查验结果
            role_info["seer_results"] = self.seer_results.copy()
        
        elif player.role == "狼人":
            # 狼人知道其他狼人的身份和共同的杀人行动
            role_info["werewolf_teammates"] = [
                {"player_id": p.id, "name": p.name} 
                for p in self.werewolves if p.id != player.id
            ]
            role_info["werewolf_kills"] = {}
            for day, result in self.night_results.items():
                if "werewolf_kill" in result["actions"]:
                    kill_target = result["actions"]["werewolf_kill"]
                    role_info["werewolf_kills"][day] = {
                        "target_id": kill_target.id if hasattr(kill_target, 'id') else None,
                        "target_name": kill_target.name if hasattr(kill_target, 'name') else None
                    }
        
        elif player.role == "女巫":
            # 女巫知道自己的药品使用情况
            role_info["potion_usage"] = {
                "has_antidote": player.has_antidote,
                "has_poison": player.has_poison,
                "usage_history": {}
            }
            for day, result in self.night_results.items():
                day_usage = {}
                if "witch_save" in result["actions"]:
                    save_target = result["actions"]["witch_save"]
                    day_usage["saved"] = {
                        "target_id": save_target.id if hasattr(save_target, 'id') else None,
                        "target_name": save_target.name if hasattr(save_target, 'name') else None
                    }
                if "witch_poison" in result["actions"]:
                    poison_target = result["actions"]["witch_poison"]
                    day_usage["poisoned"] = {
                        "target_id": poison_target.id if hasattr(poison_target, 'id') else None,
                        "target_name": poison_target.name if hasattr(poison_target, 'name') else None
                    }
                if day_usage:
                    role_info["potion_usage"]["usage_history"][day] = day_usage
        
        elif player.role == "守卫":
            # 守卫知道自己的守护历史
            role_info["guard_history"] = {}
            for day, result in self.night_results.items():
                if "guard_protect" in result["actions"]:
                    protect_target = result["actions"]["guard_protect"]
                    role_info["guard_history"][day] = {
                        "target_id": protect_target.id if hasattr(protect_target, 'id') else None,
                        "target_name": protect_target.name if hasattr(protect_target, 'name') else None
                    }
        
        return role_info
    
    def get_alive_players(self):
        """获取存活玩家"""
        return [p for p in self.players if p.is_alive]
    
    def get_dead_players(self):
        """获取已死亡玩家"""
        return [p for p in self.players if not p.is_alive]
    
    def kill_player(self, player):
        """杀死玩家"""
        player.die()
        if player in self.alive_players:
            self.alive_players.remove(player)
        if player not in self.dead_players:
            self.dead_players.append(player)
    
    def check_game_over(self):
        """检查游戏是否结束"""
        alive_werewolves = [p for p in self.alive_players if p.role == "狼人"]
        alive_villagers = [p for p in self.alive_players if p.role != "狼人"]
        
        if len(alive_werewolves) == 0:
            self.game_over = True
            self.winner = "村民"
            return True
        elif len(alive_werewolves) >= len(alive_villagers):
            self.game_over = True
            self.winner = "狼人"
            return True
        
        return False
    
    def reset_votes(self):
        """重置投票"""
        self.votes = {}
        for player in self.players:
            player.reset_votes()
    
    def add_vote(self, voter, target):
        """添加投票"""
        self.votes[voter.id] = target.id
        target.votes_received += 1
    
    def get_vote_result(self):
        """获取投票结果"""
        if not self.votes:
            return None
        
        vote_counts = Counter(self.votes.values())
        max_votes = max(vote_counts.values())
        candidates = [player_id for player_id, votes in vote_counts.items() if votes == max_votes]
        
        if len(candidates) == 1:
            # 找到被投票最多的玩家
            target_id = candidates[0]
            return next(p for p in self.alive_players if p.id == target_id)
        else:
            # 平票情况，随机选择一个
            target_id = random.choice(candidates)
            return next(p for p in self.alive_players if p.id == target_id)
    
    def next_phase(self):
        """进入下一阶段"""
        if self.phase == "day":
            self.phase = "voting"
        elif self.phase == "voting":
            self.phase = "night"
        elif self.phase == "night":
            self.phase = "day"
            self.day += 1
    
    def to_dict(self):
        """转换为字典格式，用于传递给AI"""
        return {
            "day": self.day,
            "phase": self.phase,
            "alive_players": self.alive_players,
            "dead_players": self.dead_players,
            "total_players": len(self.players)
        }