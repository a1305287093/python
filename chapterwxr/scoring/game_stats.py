class GameStats:
    """追踪外星人入侵的统计数据"""
    
    def __init__(self, ai_game):
        """初始化统计"""
        self.settings = ai_game.settings
        self.reset_stats()

        # 以不活动状态开始游戏
        self.game_active = False

        # 高分不被重置
        self.high_score = 0
        
    def reset_stats(self):
        """初始化在游戏中可以改变的统计数据"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1