

class BaseGame:
    # 玩家和分数
    players: dict[int, float]
    onFinishCallback = None

    def __init__(self):
        self.players = dict()

    def join(self, newPlayerID: int, defaultScore: float = 0.0):
        if newPlayerID not in self.players:
            self.players[newPlayerID] = defaultScore

    def addScore(self, playerID: int, score: float):
        self.join(playerID)
        self.players[playerID] += score

    async def start(self):
        pass
    
    async def finish(self):
        if (self.onFinishCallback):
            self.onFinishCallback()
