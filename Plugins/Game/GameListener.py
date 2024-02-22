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
        await game_starter.finish("请输入游戏名！")

    ret = await GameManager.startGameByName(bot, event.group_id, args)
    await game_starter.finish(ret)
