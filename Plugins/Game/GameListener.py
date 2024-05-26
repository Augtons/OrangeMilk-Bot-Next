from nonebot import *
from nonebot.rule import *
from nonebot.adapters.onebot.v11 import *

from Utils import utils
from . import GameManager

config = get_plugin_config(Config)

game_starter = on(rule=is_type(GroupMessageEvent))
@game_starter.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    cmds, args = utils.parse_command(event.get_message())
    if ("/game" not in cmds):
        await game_starter.finish()

    if (len(args) == 0):
        msg = "请输入“/game 游戏名”以启动群游戏！\n\n当前支持的游戏：\n"
        for index, name in enumerate(GameManager.getAllGamesName()):
            msg += f"【{index + 1}】 {name}\n"

        await game_starter.finish(msg)

    ret = await GameManager.startGameByName(bot, event.group_id, args)
    await game_starter.finish(ret)
