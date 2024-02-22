from pydantic import *
from nonebot import logger

class Config(BaseModel):
    master_qqs: list[int]

    @field_validator("master_qqs")
    @classmethod
    def check_master_qq(cls, qq: list[int]) -> list[int]:
        logger.info("+++++++++++++++++++++")
        logger.info("Bot 主人QQ: {}".format(qq))
        logger.info("+++++++++++++++++++++")
        return qq