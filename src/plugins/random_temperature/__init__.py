from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

from . import temperature
random_temperature=on_command("体温",aliases={"随机体温","随机温度"},priority=3,block=True)

@random_temperature.handle()
async def _random_temperature(bot:Bot,event:MessageEvent):
    '''
    随机体温，写着玩的
    '''
    tem = await temperature.get_tem()
    await random_temperature.send(message=str(tem))
