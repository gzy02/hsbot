from nonebot import on_command, on_fullmatch, on_regex, on_startswith
minion_query = on_startswith(msg=("查随从 "), priority=2, block=False)
cards_query = on_startswith(msg=("查卡牌 "), priority=2, block=False)
jjc_aomi_query=on_startswith(msg=("jjc奥秘 ","竞技场奥秘 ","jjc查奥秘 ","竞技场查奥秘 " ,"jjc猜奥秘 ","猜奥秘jjc ","竞技场猜奥秘 "),priority=3,block=True)
jjc_choose=on_startswith(msg=("竞技场选牌 ","jjc选牌 ","选牌 ","jjc "),priority=4,block=True)
class_performance = on_startswith(msg=("查胜率 "), priority=3, block=False)
build_cards=on_regex(pattern=".*?AAE[BCD]A.*", priority=3, block=True)
pic_query=on_startswith(msg=("查卡图 ","查图片 ","查牌面 ","查卡面 ","查描述 "),priority=4,block=True)

all_set_query=on_fullmatch(msg=("查系列","查询所有系列"),priority=1,block=True)
jjcCardsSet_query=on_fullmatch(msg=("当前jjc环境","jjc环境","当前jjc系列","jjc系列","查jjc系列","查jjc系列","查系列jjc","查系列 jjc"),priority=1,block=True)

#管理员相关
reset_database=on_fullmatch(msg="重置数据库",priority=1,block=True)
reset_jjcCardsSet=on_startswith(msg=("重置jjc ","重置jjc系列 ","重置jjc环境 "),priority=1,block=True)
add_admin=on_startswith(msg=("添加管理员 "),priority=4,block=True)
delete_admin=on_startswith(msg=("删除管理员 "),priority=4,block=True)
admin_query=on_fullmatch(msg=("查询管理员","管理员查询"),priority=9,block=True)

from .handle import *
from .admin_handle import *
from .pic_handle import *
