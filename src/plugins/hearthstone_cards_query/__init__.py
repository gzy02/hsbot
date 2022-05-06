from nonebot import on_command, on_startswith

minion_query = on_startswith(msg=("查随从"), priority=2, block=False)
cards_query = on_startswith(msg=("查卡牌"), priority=1, block=False)
jjc_aomi_query=on_startswith(msg=("jjc奥秘","竞技场奥秘","jjc查奥秘","竞技场查奥秘"),priority=3,block=False)
from .handle import *
