from nonebot import on_command, on_fullmatch, on_regex, on_startswith
reset_database=on_startswith(msg="重置数据库",priority=1,block=True)
minion_query = on_startswith(msg=("查随从 "), priority=2, block=False)
cards_query = on_startswith(msg=("查卡牌 "), priority=1, block=False)
jjc_aomi_query=on_startswith(msg=("jjc奥秘 ","竞技场奥秘 ","jjc查奥秘 ","竞技场查奥秘 " ,"jjc猜奥秘 ","猜奥秘jjc ","竞技场猜奥秘 "),priority=3,block=True)
jjc_choose=on_startswith(msg=("竞技场选牌 ","jjc选牌 ","选牌 ","jjc "),priority=4,block=True)
class_performance = on_startswith(msg=("查胜率 "), priority=3, block=False)
build_cards=on_regex(pattern=".*?AAE[BCD]A.*", priority=3, block=True)
pic_query=on_startswith(msg=("查卡图 ","查图片 ","查牌面 ","查卡面 ","查描述 "),priority=4,block=True)
jjcCardsSet_query=on_fullmatch(msg=("查系列","全系列"))



from .handle import *
from .admin_handle import *
#各系列名称可参考https://iyingdi.com/tz/post/5172746