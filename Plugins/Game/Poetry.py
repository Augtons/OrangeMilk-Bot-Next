import os, random, asyncio, time, math
from contextlib import closing
from dataclasses import dataclass
import functools
from nonebot import *
from nonebot.rule import *
from nonebot.adapters.onebot.v11 import *
import sqlite3

from .BaseGame import BaseGame

feihualingRepoFilePath = os.path.join(os.path.dirname(__file__), "DataBases", "fei_hua_ling_repo.db")

name = "飞花令"
alias = ["诗词"]

poetry_database = sqlite3.connect(feihualingRepoFilePath)

# 飞花令所有 Keyword
words = []
with closing(poetry_database.cursor()) as cursor:
    cursor.execute("select word from fhl_words")
    words = [row[0] for row in cursor]

@dataclass
class PoetrySentence():
    book: str
    sentence: str
    title: str
    author: str

def get_poetry_entity(sentence: str) -> PoetrySentence | None:
    """
    工具函数，根据子句从数据库中检索诗词对象
    """
    global poetry_database
    with closing(poetry_database.cursor()) as cursor:
        cursor.execute("select * from fhl_poetry w where w.sub_sentence = ?", (sentence,))
        sentence_objs = cursor.fetchall()
    if len(sentence_objs) < 1:
        return None
    else:
        sentence_row = sentence_objs[0]
        return PoetrySentence(
            book=sentence_row[5],
            sentence=sentence_row[2],
            title=sentence_row[3],
            author=sentence_row[4]
        )

class PoetryGame(BaseGame):
    def __init__(self, bot: Bot, groupId):
        super().__init__(bot=bot, groupId=groupId)
        self.matcher = on(rule=is_type(GroupMessageEvent))
        self.timer = None
        self.remainTime = 120
        self.currentWord = random.choice(words)
        self.usedSentence = set()
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
            MessageSegment.text(f"{name}游戏开始！") + MessageSegment.face(178) + 
            MessageSegment.text("\n\n【帮助】\n根据题目中提供的字，对出包含此字的诗句。\n\n范围：《唐诗三百首》、《全唐诗》、《全宋诗》、《全宋词》、《南唐二主词》、《诗经》、《楚辞》、《曹操诗集》、《花间集》、《纳兰性德诗集》、部分元曲")
        )
        await self.send("本局抽到的题目是: {}".format(self.currentWord))
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
                await self.send(f"还剩一分钟了\n\n输入“排名”可查看当前排名\n请回答含有“{self.currentWord}”的诗句")
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
                MessageSegment.text(f"\n\n游戏已进行: {self.calculate_running_time()}分钟\n请回答含有“{self.currentWord}”的诗句")
            )

        if msg in self.usedSentence:
            await self.matcher.finish(
                MessageSegment.at(str(event.user_id)) +
                MessageSegment.text(f"\n“{msg}”这句有人回答过了哦\n\n换一句含有“{self.currentWord}”的诗句吧")
            )

        if self.currentWord not in msg:
            await self.matcher.finish()

        poetry_sentence = get_poetry_entity(msg)
        if poetry_sentence == None:
            await self.matcher.finish()

        self.usedSentence.add(msg)
        self.remainTime = 120
        self.addScore(event.user_id, +1.0)
        await self.matcher.finish(
            MessageSegment.text("恭喜 ") + MessageSegment.at(str(event.user_id)) + " 回答正确" + MessageSegment.face(178) +
            f"\n当前分数为{self.players[event.user_id]} (+1.0)\n\n" +
            f"此句出自：《{poetry_sentence.book}》\n" +
            f"{poetry_sentence.sentence}\n" +
            f"　——《{poetry_sentence.title}》({poetry_sentence.author})"
        )
