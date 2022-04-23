import random

async def get_tem() -> float:
    """
    :return: 随机体温
    """
    return round(random.random()+36.3,1)
