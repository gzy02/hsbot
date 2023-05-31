from nonebot import on_request
from nonebot.adapters.onebot.v11 import Bot, RequestEvent, FriendRequestEvent, GroupRequestEvent
from nonebot.log import logger


async def _is_add_friend(bot: Bot, event: RequestEvent):
    #print(event.get_event_description())
    return isinstance(event, FriendRequestEvent)


add_friend = on_request(_is_add_friend, block=False, priority=100)


@add_friend.handle()
async def _add_friend(bot: Bot, event: FriendRequestEvent):
    #print(event.get_event_description())
    return await event.approve(bot)

"""
async def _is_add_group(bot: Bot, event: RequestEvent):
    #print(event.get_event_description())
    return isinstance(event, GroupRequestEvent)


add_group = on_request(_is_add_group, block=False, priority=2)


@add_group.handle()
async def _add_group(bot: Bot, event: GroupRequestEvent):
    #print(event.get_event_description())
    await event.reject(bot)
"""