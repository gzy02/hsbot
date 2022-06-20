#管理员才有权限的操作
from .utility import verify_admin,connect_and_close_database,SYSTEM_ADMIN_QQ_NUMBER,JJCCardsSetPath,admin_qq_number_json_path,database_enable
from . import reset_database,jjcCardsSet_query,all_set_query,reset_jjcCardsSet,delete_admin,add_admin
from . import models
from . import init_database_from_json
from . import ask_json
from . import query
from nonebot.adapters.onebot.v11 import Bot, MessageEvent,Message
import os
import json

@reset_database.handle()
@connect_and_close_database
@verify_admin(Matcher=reset_database)#必须是管理员才行
async def _reset_database(bot: Bot, event: MessageEvent):
    """重置数据库"""
    try:
        global database_enable#全局
        res_str="开始重置..."
        if event.message_type=="group":
            res_str=f'[CQ:at,qq={event.get_user_id()}]'+res_str
        await reset_database.send(message=Message(res_str))

        database_enable=False
        
        if models.MINIONCards.table_exists:
            models.MINIONCards.drop_table()
        if models.SPELLCards.table_exists:
            models.SPELLCards.drop_table()
        if models.HEROCards.table_exists:
            models.HEROCards.drop_table()
        if models.WEAPONCards.table_exists:
            models.WEAPONCards.drop_table()
        if models.Cards.table_exists:
            models.Cards.drop_table()

        models.Cards.create_table()
        models.MINIONCards.create_table()
        models.SPELLCards.create_table()
        models.WEAPONCards.create_table()
        models.HEROCards.create_table()

        json_url = "./json_file/cards.collectible.json"
        ask_json.get_cards_json(json_url)
        init_database_from_json.init_database_from_json(json_url)
        database_enable=True
        if os.path.exists(json_url):
            os.remove(json_url)
            
        res_str="重置完成"
        if event.message_type=="group":
            res_str=f'[CQ:at,qq={event.get_user_id()}]'+res_str
        await reset_database.send(message=Message(res_str))

    except Exception as e:
        await reset_database.finish((f'[重置数据库]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}'))
        

@all_set_query.handle()
@connect_and_close_database
async def _all_set_query(bot: Bot, event: MessageEvent):
    """查系列/全系列"""
    try:
        message="当前炉石所有系列如下：\n"
        cnt=1
        for i in query.find_all_set():
            message+=str(cnt)+'.'+i.set+'\n'
            cnt+=1
        message+="重置jjc系列时，请完整依照上述系列名填写"
        await all_set_query.send(message=message)
    except Exception as e:
        await all_set_query.finish((f'[查系列]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}'))
        

@jjcCardsSet_query.handle()
@connect_and_close_database
async def _jjcCardsSet_query(bot: Bot, event: MessageEvent):
    """查询当前JJCCardsSet"""
    try:
        with open(JJCCardsSetPath, "r", encoding="utf8") as fd:
            JJCCardsSet = json.loads(fd.read())["JJCCardsSet"]
    except Exception as e:
        jjcCardsSet_query.finish(f"[查系列jjc]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}")
    try:
        message="当前jjc环境中，所有系列如下：\n"
        cnt=1
        for i in JJCCardsSet:
            message+=str(cnt)+'.'+i+'\n'
            cnt+=1
        await jjcCardsSet_query.send(message=message)
    except Exception as e:
        await jjcCardsSet_query.finish((f'[查系列jjc]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}'))
        
@delete_admin.handle()
async def _delete_admin(bot: Bot, event: MessageEvent):
    if str(SYSTEM_ADMIN_QQ_NUMBER)!=event.get_user_id():
        message=f'您不是hsbot的系统管理员哦，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]'
        if event.message_type=="group":
            message=f'[CQ:at,qq={event.get_user_id()}]'+message
        await delete_admin.finish(Message(message=message))
    else:
        pass