#管理员才有权限的操作
from .utility import verify_admin,connect_and_close_database,SYSTEM_ADMIN_QQ_NUMBER,JJCCardsSetPath,admin_qq_number_json_path,database_enable
from . import reset_database,jjcCardsSet_query,all_set_query,reset_jjcCardsSet,delete_admin,add_admin,admin_query
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
    """查系列"""
    try:
        message="当前炉石所有系列如下：\n"
        cnt=1
        for i in query.find_all_set():
            message+=str(cnt)+'.'+i.set+'\n'
            cnt+=1
        message+="重置jjc系列时，请完整依照上述系列名填写\n"
        message+="各系列名称可参考https://iyingdi.com/tz/post/5172746"
        await all_set_query.send(message=message)
    except Exception as e:
        await all_set_query.finish((f'[查系列]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}'))
        

@jjcCardsSet_query.handle()
async def _jjcCardsSet_query(bot: Bot, event: MessageEvent):
    """查询当前JJCCardsSet"""
    try:
        with open(JJCCardsSetPath, "r", encoding="utf8") as fd:
            JJCCardsSet:list = json.loads(fd.read())["JJCCardsSet"]
    except Exception as e:
        jjcCardsSet_query.finish(f"[查系列jjc]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}")
    try:
        message="当前jjc环境中，所有系列如下：\n"
        cnt=1
        for i in JJCCardsSet:
            message+=str(cnt)+'.'+i+'\n'
            cnt+=1
        message+="各系列名称可参考https://iyingdi.com/tz/post/5172746"
        await jjcCardsSet_query.send(message=message)
    except Exception as e:
        await jjcCardsSet_query.finish((f'[查系列jjc]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}'))
        
@delete_admin.handle()
async def _delete_admin(bot: Bot, event: MessageEvent):
    """删除管理员"""
    try:
        if str(SYSTEM_ADMIN_QQ_NUMBER)!=event.get_user_id():#得是系统管理员
            message=f'您不是hsbot的系统管理员哦，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]使用该指令'
            if event.message_type=="group":
                message=f'[CQ:at,qq={event.get_user_id()}]'+message
            await delete_admin.send(Message(message=message))
        else:
            with open(admin_qq_number_json_path, "r", encoding="utf8") as fp:
                admin_qq_number = json.loads(fp.read())
                
            text=event.get_plaintext()
            text_list=text.split()
            if len(text_list)>=2:
                for i in range(1,len(text_list)):
                    if text_list[i] in admin_qq_number["admin_qq_number"]:#存在的才删去
                        admin_qq_number["admin_qq_number"].remove(text_list[i])
                with open(admin_qq_number_json_path, "w", encoding="utf8") as fp:
                    fp.write(str(admin_qq_number).replace("'",'"'))#单引号换双引号
                await delete_admin.send(f'已删除上述管理员')
            else:
                await delete_admin.send(f'您的输入有误，请输入“删除管理员 <管理员qq号列表>”')
    except Exception as e:
        await delete_admin.finish((f'[删除管理员]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}'))
        
@add_admin.handle()
@verify_admin(Matcher=add_admin)#必须是管理员才行
async def _add_admin(bot: Bot, event: MessageEvent):
    """添加管理员"""
    try:
        with open(admin_qq_number_json_path, "r", encoding="utf8") as fp:
            admin_qq_number = json.loads(fp.read())
            
        text=event.get_plaintext()
        text_list=text.split()
        if len(text_list)>=2:
            for i in range(1,len(text_list)):
                if text_list[i] not in admin_qq_number["admin_qq_number"]:#存在的才加上
                    admin_qq_number["admin_qq_number"].append(text_list[i])
            with open(admin_qq_number_json_path, "w", encoding="utf8") as fp:
                fp.write(str(admin_qq_number).replace("'",'"'))#单引号换双引号
            await add_admin.send(f'已添加上述管理员')
        else:
            await add_admin.send(f'您的输入有误，请输入“添加管理员 <管理员qq号列表>”')
    except Exception as e:
        await add_admin.finish((f'[添加管理员]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}'))

@admin_query.handle()
async def _admin_query():
    """管理员查询"""
    try:
        with open(admin_qq_number_json_path, "r", encoding="utf8") as fp:
            admin_qq_number:list = json.loads(fp.read())["admin_qq_number"]
            #admin_qq_number.append(str(SYSTEM_ADMIN_QQ_NUMBER))
            await admin_query.send("hsbot的管理员列表如下:\n"+str(admin_qq_number))
    except Exception as e:
        await admin_query.finish((f'[查询管理员]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}'))

@reset_jjcCardsSet.handle()
@connect_and_close_database
@verify_admin(Matcher=reset_jjcCardsSet)#必须是管理员
async def _reset_jjcCardsSet(bot:Bot,event:MessageEvent):
    """重置jjc"""
    try:
        JJCCardsSet_dict={"JJCCardsSet": []}
        all_set=[]#所有系列名
        for i in query.find_all_set():
            all_set.append(i.set)
        text=event.get_plaintext()
        text_list=text.split()
        if len(text_list)>=2:
            work_well=True
            for i in range(1,len(text_list)):
                if text_list[i] not in all_set:#存在的才加上
                    await reset_jjcCardsSet.send(f'您的输入有误，请检查系列名{text_list[i]}的拼写')
                    work_well=False
                    break
                else:
                    JJCCardsSet_dict["JJCCardsSet"].append(text_list[i])
            if work_well:
                with open(JJCCardsSetPath, "w", encoding="utf8") as fp:
                    fp.write(str(JJCCardsSet_dict).replace("'",'"'))#单引号换双引号
                await reset_jjcCardsSet.send(f'已重置当前jjc环境，可使用指令“查系列jjc”验证')
        else:
            await reset_jjcCardsSet.send(f'您的输入有误，请输入“重置jjc <系列名列表>”')
    except Exception as e:
        await reset_jjcCardsSet.finish((f'[重置jjc]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}'))
