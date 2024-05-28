import os, re, random, asyncio, time, math
import functools
from nonebot import *
from nonebot.rule import *
from nonebot.adapters.onebot.v11 import *

from .BaseGame import BaseGame

idiomsRepoFilePath = os.path.join(os.path.dirname(__file__), "DataBases", "idioms5w.txt")

name = "成语接龙"
alias = ["成语", "词语接龙"]

allIdiomsPinyin = {}
allIdioms = []
idiomsDict = {}

with open(idiomsRepoFilePath, encoding='utf-8') as idiomsFile:
    while True:
        line = idiomsFile.readline()
        if line == "":
            break
        idiomAndpinyin = line.split("|")
        if len(idiomAndpinyin) <= 1:
            continue
        idiom, pinyin = idiomAndpinyin[0:2]
        pinyin = re.sub(r"[āáǎà]", "a", pinyin)
        pinyin = re.sub(r"[ōóǒò]", "o", pinyin)
        pinyin = re.sub(r"[ēéěè]", "e", pinyin)
        pinyin = re.sub(r"[īíǐì]", "i", pinyin)
        pinyin = re.sub(r"[ūúǔù]", "u", pinyin)
        pinyin = re.sub(r"[ǖǘǚǜü]", "v", pinyin)

        rawPinyin = []
        for py in (py for py in (s.strip() for s in re.split(r'[\s,，]', pinyin)) if py != ""):
            rawPinyin.append(py)
        if len(rawPinyin) > 0:
            allIdiomsPinyin[idiom] = rawPinyin
            allIdioms.append(idiom)
            if rawPinyin[0] not in idiomsDict:
                idiomsDict[rawPinyin[0]] = []
            idiomsDict[rawPinyin[0]].append(idiom)

logger.info(f"[Game]成语接龙: 成语注入完毕，共 {len(allIdiomsPinyin)} 个成语")



class IdiomsGame(BaseGame):
    def __init__(self, bot: Bot, groupId):
        super().__init__(bot=bot, groupId=groupId)
        self.matcher = on(rule=is_type(GroupMessageEvent))
        self.currentIdiom = random.choice(allIdioms)
        self.timer = None
        self.remainTime = 120
        self.startTime = int(time.time())
        pass

    def calculate_running_time(self):
        """计算游戏时长（分钟）"""
        elapsed_time = int(time.time()) - self.startTime
        return math.ceil(elapsed_time / 60)

    async def send(self, msg):
        await self.bot.send_group_msg(group_id=self.group_id, message=msg)

    #[Override]
    async def start(self):
        await super().start()
        await self.send(
            MessageSegment.text("成语接龙游戏开始！") + MessageSegment.face(178) + 
            MessageSegment.text("\n\n【帮助】\n回答一个成语，使得其第一个字与上一个成语的最后一个字读音相同(音调可不同)，首尾相接不断延伸。")
        )
        await self.send("第一个成语是: {}({})".format(self.currentIdiom, allIdiomsPinyin[self.currentIdiom][-1]))
        self.matcher.append_handler(self.handler)
        self.remainTime = 120
        self.timer = asyncio.create_task(self.timer_coroutine())

    #[Override]
    async def finish(self):
        global name
        await super().finish()
        self.matcher.destroy()
        await self.send(
            MessageSegment.text("游戏结束！\n\n【排名】\n") +
            await self.getRank() +
            MessageSegment.text(f"\n\n本次游戏时长: {self.calculate_running_time()}分钟\n输入“/game {name}”重新开始")
        )
        atMsgs = functools.reduce(lambda a, b: a + b, (MessageSegment.at(qq) for qq in self.players.keys()))
        await self.send(atMsgs)
        if (self.timer != None):
            self.timer.cancel()

    async def timer_coroutine(self):
        while self.remainTime >= 1:
            self.remainTime -= 1
            if (self.remainTime == 60):
                await self.send(f"还剩一分钟了\n\n输入“排名”可查看当前排名\n当前成语是: {self.currentIdiom}({allIdiomsPinyin[self.currentIdiom][-1]})")
            elif (self.remainTime == 30):
                await self.send(f"还剩 30 秒了");
            elif (self.remainTime == 0):
                await self.finish()
            await asyncio.sleep(1)

    async def handler(self, event: GroupMessageEvent):
        if event.group_id != self.group_id:
            await self.matcher.finish()
        msg = event.get_plaintext().strip()

        if msg in ("退出", "结束"):
            if self.remainTime > 30:
                await self.send(f"距离上次有人回答还很近哦，再等 {self.remainTime - 30} 秒再结束吧")
            else:
                await self.finish()
            return
        
        if msg in ("排名", "状态"):
            await self.matcher.finish(
                MessageSegment.text("当前排名: \n") +
                MessageSegment.text(await self.getRank()) +
                MessageSegment.text(f"\n\n游戏已进行 {self.calculate_running_time()} 分钟\n当前成语: {self.currentIdiom}({allIdiomsPinyin[self.currentIdiom][-1]})")
            )
        
        if msg in idiomsDict[allIdiomsPinyin[self.currentIdiom][-1]]:
            self.remainTime = 120
            self.currentIdiom = msg
            self.addScore(event.user_id, +1.0)
            await self.matcher.finish(
                MessageSegment.text("恭喜 ") + MessageSegment.at(str(event.user_id)) + " 回答正确" + MessageSegment.face(178) +
                f"\n当前分数为 {self.players[event.user_id]} (+1.0)\n\n" +
                f"新成语: {self.currentIdiom}({allIdiomsPinyin[self.currentIdiom][-1]})"
            )
