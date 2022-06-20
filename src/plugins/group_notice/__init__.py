
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import Bot,RequestEvent,FriendRequestEvent,GroupRequestEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment

"""
[notice.group_increase.approve]: {
    'time': 1655716407, 
    'self_id': 2149627292, 
    'post_type': 'notice', 
    'notice_type': 'group_increase', 
    'sub_type': 'approve', 
    'user_id': 2149627292, 
    'group_id': 649655353, 
    'operator_id': 0
}
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2020-09-18 00:00:13
@LastEditors    : yanyongyu
@LastEditTime   : 2021-01-01 17:46:15
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER
from nonebot import get_driver, on_command, on_notice, on_message
from nonebot.adapters.onebot.v11 import Bot,GroupIncreaseNoticeEvent


async def _group_increase(bot: Bot, event: Event) -> bool:
    return isinstance(event, GroupIncreaseNoticeEvent)


group_increase = on_notice(_group_increase, priority=10, block=True)
@group_increase.handle()
async def _group_increase(bot: Bot, event: GroupIncreaseNoticeEvent):
    return await group_increase.send(MessageSegment.at(event.get_user_id())+"欢迎新朋友~")

