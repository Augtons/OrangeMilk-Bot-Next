import datetime
from nonebot import *
from nonebot.rule import *
from nonebot.adapters.onebot.v11 import *

config = get_plugin_config(Config)

alive = on(rule=is_type(LifecycleMetaEvent))
@alive.handle()
async def on_alive_handler(bot: Bot, event: LifecycleMetaEvent):
    if event.sub_type != "connect":
        await alive.finish()

    date_and_time = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    for master in config.master_qqs:
        await bot.send_private_msg(user_id=master, message="我上线了！\n{}".format(date_and_time))
    await alive.finish()


debug = on(rule=is_type(PrivateMessageEvent))
@debug.handle()
async def on_debug_handler(bot: Bot, event: PrivateMessageEvent):
    if int(event.get_user_id()) not in config.master_qqs:
        await debug.finish()

    await debug.send(
        MessageSegment.text("你小子给我发东西是吧") +
        MessageSegment.face(178)
    )
    await debug.send(
        MessageSegment.text("你发的内容转文本是：\n") +
        MessageSegment.text(str(event.get_message()))
    )
    await debug.finish(event.get_message())
