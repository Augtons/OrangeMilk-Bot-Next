from nonebot.adapters.onebot.v11 import *

def parse_command(messages: Message, prefix: str = "/") -> tuple[list[str], list[str]]:
    plainTextMsgs = [str(msg).strip() for msg in messages if msg.type == 'text']
    plainTexts = []
    for s in plainTextMsgs:
        plainTexts += s.split()

    commands = []
    arguments = []
    for item in plainTexts:
        if item.startswith(prefix):
            commands.append(item)
        else:
            arguments.append(item)
    return (commands, arguments)