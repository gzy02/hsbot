from nonebot import on_command, on_startswith
reset_database=on_startswith(msg="重置数据库",priority=1,block=True)
minion_query = on_startswith(msg=("查随从"), priority=2, block=False)
cards_query = on_startswith(msg=("查卡牌"), priority=1, block=False)
jjc_aomi_query=on_startswith(msg=("jjc奥秘","竞技场奥秘","jjc查奥秘","竞技场查奥秘","jjc猜奥秘","竞技场猜奥秘"),priority=3,block=True)
jjc_choose=on_startswith(msg=("竞技场选牌","jjc选牌","选牌","jjc"),priority=4,block=True)

from .handle import *
