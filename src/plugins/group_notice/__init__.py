
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import Bot,Event,RequestEvent,FriendRequestEvent,GroupRequestEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment

from nonebot import get_driver, on_command, on_notice, on_message
from nonebot.adapters.onebot.v11 import Bot,GroupIncreaseNoticeEvent


async def _group_increase(bot: Bot, event: Event) -> bool:
    return isinstance(event, GroupIncreaseNoticeEvent)


group_increase = on_notice(_group_increase, priority=10, block=True)
@group_increase.handle()
async def _group_increase(bot: Bot, event: GroupIncreaseNoticeEvent):
    return await group_increase.send(MessageSegment.at(event.get_user_id())+"欢迎新朋友~")

