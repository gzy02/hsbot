import nonebot
from functools import wraps
import json
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment,Message
from . import models
from time import sleep
#管理员qq号json文件地址
admin_qq_number_json_path="./json_file/admin_qq_number.json"
#jjc卡组系列json文件地址
JJCCardsSetPath="./json_file/JJCCardsSet.json"
#系统管理员QQ号，这里直接存内存了
driver = nonebot.get_driver()
global_config = driver.config
config=global_config.dict()
SYSTEM_ADMIN_QQ_NUMBER=config['system_admin_qq_number']

database_enable=True#是否允许访问数据库
#全名对应英文名
cardClassMap = {"法师": "MAGE", "猎人": "HUNTER", "牧师": "PRIEST", "术士": "WARLOCK", "潜行者": "ROGUE",
                "德鲁伊": "DRUID", "萨满": "SHAMAN", "战士": "WARRIOR", "圣骑士": "PALADIN", "恶魔猎手": "DEMONHUNTER"}
#别名
aliasesClassMap = {"法": "法师", "猎": "猎人", "牧": "牧师", "战": "战士", "贼": "潜行者", "德": "德鲁伊",
                                   "萨": "萨满祭司", "萨满": "萨满祭司", "术": "术士", "骑士": "圣骑士", "骑": "圣骑士", "瞎": "恶魔猎手", "瞎子": "恶魔猎手"}

from typing import Any, Set, Dict, List, Type, Tuple, Union, Optional
from nonebot.matcher import Matcher
def verify_admin(Matcher:Type[Matcher]):
    """验证是否是管理员或系统管理员
    
    Args:
        Matcher (Type[Matcher]): 事件响应器类
    """
    def verify_admin_decorator(func):
        @wraps(func)
        async def wrapped_function(*args,**kwargs):
            try:
                event: MessageEvent=kwargs['event']
                fd = open(admin_qq_number_json_path, "r", encoding="utf8")
                admin_qq_number:list = json.loads(fd.read())["admin_qq_number"]
                fd.close()
            except:
                await Matcher.finish(f'[管理员验证]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]')
            admin_qq_number.append(str(SYSTEM_ADMIN_QQ_NUMBER))#系统管理员也得加上去
            if event.get_user_id() not in admin_qq_number:
                message=f'您不是hsbot的管理员哦，请联系管理员使用该指令~[CQ:face,id=178]\n管理员QQ号列表：{str(admin_qq_number)}'
                if event.message_type=="group":
                    message=f'[CQ:at,qq={event.get_user_id()}]'+message
                await Matcher.finish(Message(message))
            await func(*args,**kwargs)
        return wrapped_function
    return verify_admin_decorator

def connect_and_close_database(func):
    """
    装饰器，用于连接和断开数据库
    """
    @wraps(func)
    async def wrapped_function(*args, **kwargs):
        sleep_cnt=0
        while database_enable==False:
            sleep(1)
            sleep_cnt+=1
            if sleep_cnt>10:#很快数据库就重置完了，不急，让用户等至多10秒
                break

        # 连接数据库
        if models.database.is_closed():
            models.database.connect()
        
        await func(*args, **kwargs)
        
        # 请求结束，关数据库
        if not models.database.is_closed():
            models.database.close()
    return wrapped_function
