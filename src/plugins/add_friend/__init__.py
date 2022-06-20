
from nonebot import on_request
from nonebot.adapters.onebot.v11 import Bot,RequestEvent,FriendRequestEvent,GroupRequestEvent
from nonebot.log import logger

"""
[request.friend]: {'time': 1655710128, 'self_id': 2457256025, 'post_type': 'request', 'request_type': 'friend', 'user_id': 1262454489, 'comment': 'gzy', 'flag': '1655710202000000'}
[request.group.invite]: {'time': 1655716407, 'self_id': 2149627292, 'post_type': 'request', 'request_type': 'group', 'sub_type': 'invite', 'group_id': 649655353, 'user_id': 1262454489, 'comment': '', 'flag': '1655716481425881'}
"""
async def _is_add_friend(bot: Bot, event: RequestEvent):
    print(event.get_event_description())
    return isinstance(event,FriendRequestEvent)

add_friend=on_request(_is_add_friend,block=False,priority=1)
@add_friend.handle()
async def _add_friend(bot: Bot, event: FriendRequestEvent):
    print(event.get_event_description())
    return await event.approve(bot)

async def _is_add_group(bot: Bot, event: RequestEvent):
    print(event.get_event_description())
    return isinstance(event,GroupRequestEvent)

add_group=on_request(_is_add_group,block=False,priority=2)
@add_group.handle()
async def _add_group(bot: Bot, event: GroupRequestEvent):
    print(event.get_event_description())
    try:
        await event.approve(bot)
    except:
        logger.info('已经进群了')