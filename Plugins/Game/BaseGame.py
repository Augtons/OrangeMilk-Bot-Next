from nonebot import *
from nonebot.rule import *
from nonebot.adapters.onebot.v11 import *

class BaseGame:
    # 玩家和分数
    players: dict[int, float]
    onFinishCallback = None

    def __init__(self, bot: Bot, groupId):
        self.players = dict()
        self.bot = bot
        self.group_id = groupId

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

    async def getRank(self):
        scores = [item for item in self.players.items()]
        scores.sort(key=lambda item: -item[1])
        ranks = []
        for index, (qq, score) in enumerate(scores):
            info = await self.bot.get_group_member_info(group_id=self.group_id, user_id=qq, no_cache=True)
            name = info["card"] if ("card" in info and info["card"] != None) else info["nickname"]
            ranks.append((index + 1, name, score))
        if (len(ranks) > 0):
            return "\n".join(("【{}】{}\n    得分: {}".format(rank, name, score) for (rank, name, score) in ranks))
        else:
            return "暂无排名"
