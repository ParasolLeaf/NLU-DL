"""
狼人杀游戏主逻辑
"""
import asyncio
import random
import re
from colorama import init, Fore, Back, Style
from game.game_state import GameState

# 初始化colorama
init()


class WerewolfGame:
    def __init__(self, players):
        self.players = players
        self.game_state = GameState(players)
        self.assign_roles()
    
    def assign_roles(self):
        """分配角色"""
        roles = ["狼人", "狼人", "狼人", "预言家", "女巫", "守卫", "村民", "村民"]
        random.shuffle(roles)
        
        for i, player in enumerate(self.players):
            player.role = roles[i]
        
        # 更新游戏状态中的角色分组
        self.game_state.werewolves = [p for p in self.players if p.role == "狼人"]
        self.game_state.villagers = [p for p in self.players if p.role != "狼人"]
    
    def print_game_info(self):
        """打印游戏信息"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"狼人杀游戏 - 第{self.game_state.day}天 - {self.game_state.phase.upper()}阶段")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}存活玩家 ({len(self.game_state.alive_players)}人):")
        for player in self.game_state.alive_players:
            role_color = Fore.RED if player.role == "狼人" else Fore.BLUE
            print(f"  {role_color}{player.id}号 - {player.name} ({player.role}){Style.RESET_ALL}")
        
        if self.game_state.dead_players:
            print(f"\n{Fore.YELLOW}已淘汰玩家:")
            for player in self.game_state.dead_players:
                print(f"  {Fore.YELLOW}{player.id}号 - {player.name} ({player.role}){Style.RESET_ALL}")
    
    async def run_game(self):
        """运行游戏主循环"""
        print(f"{Fore.MAGENTA}🎮 8人狼人杀游戏开始！{Style.RESET_ALL}")
        self.print_roles()
        
        # 第一天直接进入夜晚阶段
        print(f"\n{Fore.YELLOW} 第一天直接进入夜晚阶段，没有白天发言和投票{Style.RESET_ALL}")
        self.game_state.phase = "night"
        
        while not self.game_state.check_game_over():
            self.print_game_info()
            
            if self.game_state.phase == "day":
                await self.day_phase()
            elif self.game_state.phase == "voting":
                await self.voting_phase()
            elif self.game_state.phase == "night":
                await self.night_phase()
            
            self.game_state.next_phase()
            
            # 检查游戏是否结束
            if self.game_state.check_game_over():
                break
        
        self.print_game_result()
    
    def print_roles(self):
        """打印角色分配"""
        print(f"\n{Fore.CYAN} 角色分配：{Style.RESET_ALL}")
        for player in self.players:
            role_color = Fore.RED if player.role == "狼人" else Fore.BLUE
            print(f"  {role_color}{player.id}号 - {player.name}: {player.role}{Style.RESET_ALL}")
    
    async def day_phase(self):
        """白天阶段 - 自由发言（第二天开始）"""
        print(f"\n{Fore.YELLOW} 白天阶段 - 自由发言{Style.RESET_ALL}")
        
        # 随机打乱发言顺序
        speaking_order = self.game_state.alive_players.copy()
        random.shuffle(speaking_order)
        
        for player in speaking_order:
            # 获取该玩家的游戏历史
            game_history = self.game_state.get_game_history_for_player(player)
            game_history["current_day"] = self.game_state.day
            
            prompt = f"现在是白天自由发言阶段，请发表你的看法和分析。你可以分享信息、质疑其他玩家或为自己辩护。请根据已知的游戏历史信息进行分析。"
            
            try:
                response = await player.speak(prompt, self.game_state.to_dict(), game_history)
                print(f"\n{Fore.GREEN}{player.id}号({player.name})说：{Style.RESET_ALL}")
                print(f"  {response}")
                
                # 记录发言
                self.game_state.add_day_speech(player, response)
                
            except Exception as e:
                print(f"\n{Fore.RED}{player.id}号({player.name})无法发言: {e}{Style.RESET_ALL}")
            
            # 添加延迟，让输出更清晰
            await asyncio.sleep(1)
    
    async def voting_phase(self):
        """投票阶段（第二天开始）"""
        print(f"\n{Fore.YELLOW} 投票阶段{Style.RESET_ALL}")
        
        self.game_state.reset_votes()
        
        # 每个玩家进行投票
        for voter in self.game_state.alive_players:
            # 获取该玩家的游戏历史
            game_history = self.game_state.get_game_history_for_player(voter)
            game_history["current_day"] = self.game_state.day
            
            candidates = [p for p in self.game_state.alive_players if p != voter]
            candidate_list = ", ".join([f"{p.id}号({p.name})" for p in candidates])
            
            prompt = f"现在是投票阶段，你需要投票淘汰一名玩家。候选人：{candidate_list}。请根据今天的发言和历史信息分析，说明你的投票理由，并在最后明确说出：'我投票给X号玩家'"
            
            try:
                response = await voter.speak(prompt, self.game_state.to_dict(), game_history)
                print(f"\n{Fore.BLUE}{voter.id}号({voter.name})的投票：{Style.RESET_ALL}")
                print(f"  {response}")
                
                # 解析投票目标
                target = self.parse_vote(response, candidates)
                if target:
                    self.game_state.add_vote(voter, target)
                    print(f"  {Fore.CYAN}→ 投票给{target.id}号({target.name}){Style.RESET_ALL}")
                else:
                    # 随机投票
                    target = random.choice(candidates)
                    self.game_state.add_vote(voter, target)
                    print(f"  {Fore.YELLOW}→ 随机投票给{target.id}号({target.name}){Style.RESET_ALL}")
                
            except Exception as e:
                print(f"\n{Fore.RED}{voter.id}号({voter.name})投票失败: {e}{Style.RESET_ALL}")
                # 随机投票
                target = random.choice(candidates)
                self.game_state.add_vote(voter, target)
                print(f"  {Fore.YELLOW}→ 随机投票给{target.id}号({target.name}){Style.RESET_ALL}")
            
            await asyncio.sleep(1)
        
        # 统计投票结果
        eliminated_player = self.game_state.get_vote_result()
        if eliminated_player:
            print(f"\n{Fore.RED} 投票结果：{eliminated_player.id}号({eliminated_player.name})被淘汰！身份是{eliminated_player.role}{Style.RESET_ALL}")
            self.game_state.kill_player(eliminated_player)
        
        # 记录投票历史
        self.game_state.add_voting_record(eliminated_player)
    
    async def night_phase(self):
        """夜晚阶段"""
        print(f"\n{Fore.BLUE} 夜晚阶段{Style.RESET_ALL}")
        
        # 狼人行动
        await self.werewolf_action()
        
        # 预言家行动
        await self.seer_action()
        
        # 女巫行动
        await self.witch_action()
        
        # 守卫行动
        await self.guard_action()
        
        # 处理夜晚结果
        await self.process_night_results()
    
    async def werewolf_action(self):
        """狼人行动 - 所有狼人共同选择一个目标"""
        alive_werewolves = [p for p in self.game_state.alive_players if p.role == "狼人"]
        if not alive_werewolves:
            return
        
        print(f"\n{Fore.RED} 狼人行动{Style.RESET_ALL}")
        
        targets = [p for p in self.game_state.alive_players if p.role != "狼人"]
        if not targets:
            return
        
        target_list = ", ".join([f"{p.id}号({p.name})" for p in targets])
        werewolf_list = ", ".join([f"{p.id}号({p.name})" for p in alive_werewolves])
        
        print(f"  {Fore.RED}存活狼人：{werewolf_list}{Style.RESET_ALL}")
        
        # 所有狼人讨论并选择目标
        werewolf_votes = {}
        for werewolf in alive_werewolves:
            # 获取狼人的游戏历史
            game_history = self.game_state.get_game_history_for_player(werewolf)
            
            prompt = f"夜晚到了，你们狼人团队需要共同选择杀死一名玩家。存活狼人：{werewolf_list}。可选目标：{target_list}。请根据白天的发言和历史信息分析，与其他狼人商议并选择目标，在回复最后明确说出：'我们选择杀死X号玩家'"
            
            try:
                response = await werewolf.speak(prompt, self.game_state.to_dict(), game_history)
                print(f"  {Fore.RED}{werewolf.id}号狼人：{response}{Style.RESET_ALL}")
                
                # 解析狼人的选择
                target = self.parse_werewolf_kill(response, targets)
                if target:
                    werewolf_votes[werewolf.id] = target
                
            except Exception as e:
                print(f"  {Fore.RED}{werewolf.id}号狼人无法行动: {e}{Style.RESET_ALL}")
        
        # 统计狼人投票，选择最多票数的目标
        if werewolf_votes:
            from collections import Counter
            vote_counts = Counter(werewolf_votes.values())
            target = vote_counts.most_common(1)[0][0]
        else:
            # 如果没有有效投票，随机选择
            target = random.choice(targets)
        
        self.game_state.night_actions["werewolf_kill"] = target
        print(f"  {Fore.RED} 狼人团队最终选择杀死{target.id}号({target.name}){Style.RESET_ALL}")
    
    async def seer_action(self):
        """预言家行动"""
        seer = next((p for p in self.game_state.alive_players if p.role == "预言家"), None)
        if not seer:
            return
        
        print(f"\n{Fore.CYAN} 预言家行动{Style.RESET_ALL}")
        
        targets = [p for p in self.game_state.alive_players if p != seer]
        target_list = ", ".join([f"{p.id}号({p.name})" for p in targets])
        
        # 获取预言家的游戏历史
        game_history = self.game_state.get_game_history_for_player(seer)
        
        prompt = f"你是预言家，可以查验一名玩家的身份。可选目标：{target_list}。请根据白天的发言和你之前的查验结果选择要查验的玩家，在回复最后明确说出：'我要查验X号玩家'"
        
        try:
            response = await seer.speak(prompt, self.game_state.to_dict(), game_history)
            print(f"  {Fore.CYAN}预言家：{response}{Style.RESET_ALL}")
            
            # 解析查验目标
            target = self.parse_seer_check(response, targets)
            if not target:
                target = random.choice(targets)
            
            # 告知查验结果
            result = "狼人" if target.role == "狼人" else "好人"
            result_prompt = f"查验结果：{target.id}号({target.name})是{result}"
            await seer.speak(result_prompt, self.game_state.to_dict())
            print(f"  {Fore.CYAN}🔍 查验{target.id}号({target.name})：{result}{Style.RESET_ALL}")
            
            # 记录查验结果
            self.game_state.add_seer_result(target, result)
            
        except Exception as e:
            print(f"  {Fore.RED}预言家行动失败: {e}{Style.RESET_ALL}")
    
    async def witch_action(self):
        """女巫行动"""
        witch = next((p for p in self.game_state.alive_players if p.role == "女巫"), None)
        if not witch:
            return
        
        print(f"\n{Fore.MAGENTA} 女巫行动{Style.RESET_ALL}")
        
        # 显示女巫当前药品状态
        antidote_status = "可用" if witch.has_antidote else "已使用"
        poison_status = "可用" if witch.has_poison else "已使用"
        print(f"  {Fore.MAGENTA}药品状态：解药({antidote_status})，毒药({poison_status}){Style.RESET_ALL}")
        
        # 如果两种药都用完了，跳过
        if not witch.has_antidote and not witch.has_poison:
            print(f"  {Fore.MAGENTA}女巫的药品已全部用完，无法行动{Style.RESET_ALL}")
            return
        
        killed_player = self.game_state.night_actions.get("werewolf_kill")
        
        # 获取女巫的游戏历史
        game_history = self.game_state.get_game_history_for_player(witch)
        
        # 构建提示信息
        if killed_player and witch.has_antidote:
            prompt = f"今晚{killed_player.id}号({killed_player.name})被狼人杀死了。"
            if witch.has_poison:
                prompt += f"你还有解药({antidote_status})和毒药({poison_status})。请根据游戏情况和历史信息决定是否要使用？回复格式：'使用解药救{killed_player.id}号' 或 '使用毒药毒X号' 或 '不使用药品'"
            else:
                prompt += f"你还有解药({antidote_status})。是否要使用解药救人？回复格式：'使用解药救{killed_player.id}号' 或 '不使用药品'"
        elif witch.has_poison:
            if killed_player:
                prompt = f"今晚{killed_player.id}号({killed_player.name})被狼人杀死了，但你的解药已用完。"
            else:
                prompt = "今晚没有人被杀死。"
            prompt += f"你还有毒药({poison_status})。请根据游戏情况决定是否要使用毒药？回复格式：'使用毒药毒X号' 或 '不使用药品'"
        else:
            return
        
        try:
            response = await witch.speak(prompt, self.game_state.to_dict(), game_history)
            print(f"  {Fore.MAGENTA}女巫：{response}{Style.RESET_ALL}")
            
            # 解析女巫的行动
            if "使用解药" in response and killed_player and witch.has_antidote:
                if witch.use_antidote():
                    self.game_state.night_actions["witch_save"] = killed_player
                    print(f"  {Fore.MAGENTA} 女巫使用解药救了{killed_player.id}号{Style.RESET_ALL}")
            elif "使用毒药" in response and witch.has_poison:
                targets = [p for p in self.game_state.alive_players if p != witch]
                poison_target = self.parse_witch_poison(response, targets)
                if not poison_target:
                    poison_target = random.choice(targets) if targets else None
                
                if poison_target and witch.use_poison():
                    self.game_state.night_actions["witch_poison"] = poison_target
                    print(f"  {Fore.MAGENTA} 女巫使用毒药毒死了{poison_target.id}号{Style.RESET_ALL}")
            else:
                print(f"  {Fore.MAGENTA}女巫选择不使用药品{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"  {Fore.RED}女巫行动失败: {e}{Style.RESET_ALL}")
    
    async def guard_action(self):
        """守卫行动"""
        guard = next((p for p in self.game_state.alive_players if p.role == "守卫"), None)
        if not guard:
            return
        
        print(f"\n{Fore.GREEN} 守卫行动{Style.RESET_ALL}")
        
        targets = [p for p in self.game_state.alive_players if p != guard]
        target_list = ", ".join([f"{p.id}号({p.name})" for p in targets])
        
        # 获取守卫的游戏历史
        game_history = self.game_state.get_game_history_for_player(guard)
        
        prompt = f"你是守卫，可以守护一名玩家。可选目标：{target_list}。请根据白天的发言和历史信息选择要守护的玩家，在回复最后明确说出：'我要守护X号玩家'"
        
        try:
            response = await guard.speak(prompt, self.game_state.to_dict(), game_history)
            print(f"  {Fore.GREEN}守卫：{response}{Style.RESET_ALL}")
            
            # 解析守护目标
            target = self.parse_guard_protect(response, targets)
            if not target:
                target = random.choice(targets)
            
            self.game_state.night_actions["guard_protect"] = target
            print(f"  {Fore.GREEN} 守卫守护了{target.id}号({target.name}){Style.RESET_ALL}")
            
        except Exception as e:
            print(f"  {Fore.RED}守卫行动失败: {e}{Style.RESET_ALL}")
    
    async def process_night_results(self):
        """处理夜晚结果"""
        print(f"\n{Fore.YELLOW} 夜晚结束，处理结果...{Style.RESET_ALL}")
        
        deaths = []
        
        # 处理狼人杀人
        killed_by_werewolf = self.game_state.night_actions.get("werewolf_kill")
        saved_by_witch = self.game_state.night_actions.get("witch_save")
        protected_by_guard = self.game_state.night_actions.get("guard_protect")
        
        if killed_by_werewolf:
            # 如果守卫守护了被女巫救的人，该人依然死亡
            if saved_by_witch == killed_by_werewolf and protected_by_guard == killed_by_werewolf:
                print(f"  {Fore.YELLOW} {killed_by_werewolf.id}号被狼人杀死，女巫使用解药救人，但守卫也守护了同一人，守卫与女巫冲突，该玩家依然死亡{Style.RESET_ALL}")
                deaths.append(killed_by_werewolf)
            elif saved_by_witch == killed_by_werewolf:
                print(f"  {Fore.CYAN} {killed_by_werewolf.id}号被狼人杀死，但被女巫救活了{Style.RESET_ALL}")
            elif protected_by_guard == killed_by_werewolf:
                print(f"  {Fore.CYAN} {killed_by_werewolf.id}号被狼人杀死，但被守卫保护了{Style.RESET_ALL}")
            else:
                deaths.append(killed_by_werewolf)
        
        # 处理女巫毒杀
        poisoned_by_witch = self.game_state.night_actions.get("witch_poison")
        if poisoned_by_witch:
            deaths.append(poisoned_by_witch)
        
        # 执行死亡
        for player in deaths:
            self.game_state.kill_player(player)
            print(f"  {Fore.RED} {player.id}号({player.name})死亡{Style.RESET_ALL}")
        
        # 记录夜晚结果
        self.game_state.add_night_result(deaths, self.game_state.night_actions)
        
        # 清空夜晚行动
        self.game_state.night_actions = {}
        
        if not deaths:
            print(f"  {Fore.GREEN} 昨夜平安无事{Style.RESET_ALL}")
    
    def parse_vote(self, response, candidates):
        """解析投票目标 - 专门解析"我投票给X号玩家"中的X，先去除空格"""
        # 先去除所有空格，然后进行解析
        cleaned_response = re.sub(r'\s+', '', response)
        
        # 使用正则表达式匹配"我投票给X号"的模式（已去除空格）
        patterns = [
            r'我投票给(\d+)号',
            r'投票给(\d+)号',
            r'选择(\d+)号',
            r'投(\d+)号'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, cleaned_response)
            if match:
                target_id = int(match.group(1))
                # 在候选人中查找对应ID的玩家
                for candidate in candidates:
                    if candidate.id == target_id:
                        return candidate
        
        # 如果正则匹配失败，尝试从原始回复的最后一句话中提取（保留原有逻辑作为备用）
        sentences = response.split('。')
        if sentences:
            last_sentence = sentences[-1].strip()
            # 同样去除空格后查找
            cleaned_last_sentence = re.sub(r'\s+', '', last_sentence)
            for candidate in candidates:
                if f"{candidate.id}号" in cleaned_last_sentence:
                    return candidate
        
        return None
    
    def parse_werewolf_kill(self, response, targets):
        """解析狼人杀人目标 - 专门解析"我们选择杀死X号玩家"中的X，先去除空格"""
        # 先去除所有空格
        cleaned_response = re.sub(r'\s+', '', response)
        
        patterns = [
            r'我们选择杀死(\d+)号',
            r'选择杀死(\d+)号',
            r'杀死(\d+)号',
            r'杀(\d+)号'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, cleaned_response)
            if match:
                target_id = int(match.group(1))
                for target in targets:
                    if target.id == target_id:
                        return target
        
        return None
    
    def parse_seer_check(self, response, targets):
        """解析预言家查验目标 - 专门解析"我要查验X号玩家"中的X，先去除空格"""
        # 先去除所有空格
        cleaned_response = re.sub(r'\s+', '', response)
        
        patterns = [
            r'我要查验(\d+)号',
            r'查验(\d+)号',
            r'检查(\d+)号'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, cleaned_response)
            if match:
                target_id = int(match.group(1))
                for target in targets:
                    if target.id == target_id:
                        return target
        
        return None
    
    def parse_witch_poison(self, response, targets):
        """解析女巫毒杀目标 - 专门解析"使用毒药毒X号"中的X，先去除空格"""
        # 先去除所有空格
        cleaned_response = re.sub(r'\s+', '', response)
        
        patterns = [
            r'使用毒药毒(\d+)号',
            r'毒药毒(\d+)号',
            r'毒死(\d+)号',
            r'毒(\d+)号'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, cleaned_response)
            if match:
                target_id = int(match.group(1))
                for target in targets:
                    if target.id == target_id:
                        return target
        
        return None
    
    def parse_guard_protect(self, response, targets):
        """解析守卫守护目标 - 专门解析"我要守护X号玩家"中的X，先去除空格"""
        # 先去除所有空格
        cleaned_response = re.sub(r'\s+', '', response)
        
        patterns = [
            r'我要守护(\d+)号',
            r'守护(\d+)号',
            r'保护(\d+)号'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, cleaned_response)
            if match:
                target_id = int(match.group(1))
                for target in targets:
                    if target.id == target_id:
                        return target
        
        return None
    
    def print_game_result(self):
        """打印游戏结果"""
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f" 游戏结束！")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        if self.game_state.winner == "狼人":
            print(f"\n{Fore.RED} 狼人获胜！{Style.RESET_ALL}")
            print(f"{Fore.RED}获胜的狼人：{Style.RESET_ALL}")
            for werewolf in self.game_state.werewolves:
                status = "存活" if werewolf.is_alive else "已死亡"
                print(f"  {werewolf.id}号 - {werewolf.name} ({status})")
        else:
            print(f"\n{Fore.BLUE} 村民获胜！{Style.RESET_ALL}")
            print(f"{Fore.BLUE}获胜的村民：{Style.RESET_ALL}")
            for villager in self.game_state.villagers:
                if villager.is_alive:
                    print(f"  {villager.id}号 - {villager.name} ({villager.role})")
        
        print(f"\n{Fore.CYAN}最终统计：{Style.RESET_ALL}")
        print(f"  游戏天数：{self.game_state.day}")
        print(f"  存活人数：{len(self.game_state.alive_players)}")
        print(f"  死亡人数：{len(self.game_state.dead_players)}")