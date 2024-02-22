import traceback
from nonebot import *
from nonebot.adapters.onebot.v11 import *
from .BaseGame import BaseGame
from . import Idioms

current_game: dict[int, tuple[str, BaseGame]] = {}

async def startGameByName(bot: Bot, group_id: int, args: list[str]) -> Message:
    if (group_id in current_game):
        return MessageSegment.text(f"""本群当前正在进行 "{current_game[group_id][0]}" 游戏哦""")
        
    if (args[0] == Idioms.name or args[0] in Idioms.alias):
        try:
            game = Idioms.IdiomsGame(bot, group_id)
            game.onFinishCallback = lambda: stopGameByName(group_id, Idioms.name)
            current_game[group_id] = (Idioms.name, game)
            await game.start()
            return None
        except Exception as e:
            traceback.print_exception(e)
            return MessageSegment.text("游戏初始化失败")
    
    return MessageSegment.text("未找到此游戏名: {}".format(args[0]))


def stopGameByName(group_id: int, name: str) -> Message:
    logger.info("群({})中的游戏{}结束".format(group_id, name))
    if (group_id in current_game and current_game[group_id][0] == name):
        del current_game[group_id]