import nonebot
from nonebot import on_command
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, Message
from . import ask_json

driver = nonebot.get_driver()
global_config = driver.config
config = global_config.dict()
SYSTEM_ADMIN_QQ_NUMBER = config['system_admin_qq_number']

sixty = on_command("60s", aliases={"早报", "60秒早报", "今日早报", "每日早报"}, priority=4, block=True)


@sixty.handle()
async def _sixty(bot: Bot, event: MessageEvent):
    """每日早报"""
    url = 'https://api.qqsuu.cn/api/dm-60s'  #'https://api.iyk0.com/60s/'  #早报url
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
    }

    res = (await ask_json.get_url(url, headers))
    if res['status'] == 1:
        message_str = ""
        if event.message_type == "group":
            message_str = f'[CQ:at,qq={event.get_user_id()}]'
        await sixty.send(message=Message(message_str) + MessageSegment.image(res['image_url']))
    else:
        await sixty.finish(f'[每日早报]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]')
