import sys, os
import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

sys.path.append(os.path.join(os.path.dirname(__file__), "Utils"))

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)


nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run()