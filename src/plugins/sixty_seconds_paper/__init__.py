import nonebot
from nonebot import on_command
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from . import ask_json

sixty = on_command("60s", aliases={"早报", "60秒早报", "今日早报"}, priority=4, block=True)


@sixty.handle()
async def _(bot: Bot, event: MessageEvent):
    url = 'https://api.iyk0.com/60s/'  #早报url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'}

    res = (await ask_json.get_url(url, headers))
    if res['status'] == 1:
        await sixty.send(message=MessageSegment.image(res['image_url']))
    else:
        logger.info('获取早报时出现错误')
