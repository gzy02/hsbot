#管理员才有权限的操作
from logging import exception
from tkinter import EXCEPTION
from .utility import verify_admin,connect_and_close_database,SYSTEM_ADMIN_QQ_NUMBER,JJCCardsSetPath,admin_qq_number_json_path,database_enable
from . import reset_database
from . import models
from . import init_database_from_json
from . import ask_json
from nonebot.adapters.onebot.v11 import Bot, MessageEvent,Message
import os

@reset_database.handle()
@connect_and_close_database
@verify_admin(Matcher=reset_database)#必须是管理员才行
async def _reset_database(bot: Bot, event: MessageEvent):
    """重置数据库"""
    try:
        res_str="开始重置..."
        if event.message_type=="group":
            res_str=f'[CQ:at,qq={event.get_user_id()}]'+res_str
        await reset_database.send(message=Message(res_str))

        database_enable=True
        
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
        database_enable=False
        if os.path.exists(json_url):
            os.remove(json_url)
            
        res_str="重置完成"
        if event.message_type=="group":
            res_str=f'[CQ:at,qq={event.get_user_id()}]'+res_str
        await reset_database.send(message=Message(res_str))

    except Exception as e:
        await reset_database.finish((f'[重置数据库]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}'))
        
