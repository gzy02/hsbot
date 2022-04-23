from nonebot import on_command, on_startswith
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.rule import to_me

from . import models

#from init_database import models
cards_query=on_startswith(msg=("查随从"),priority=1,block=False)
@cards_query.handle()
async def _(bot:Bot,event:MessageEvent):
    #连接数据库
    if models.database.is_closed():
        models.database.connect()
    
    for i in event.get_message():#获取该事件中每条消息
        print(i.data)
        if i.type=="text":#文本
            text_list=i.data['text'].split()
            if len(text_list)==2:
                if text_list[0]=="查随从":
                    try:
                        value_list=text_list[1].split('-')
                        minion_cost=value_list[0]
                        minion_attack=value_list[1]
                        minion_health=value_list[2]
                        tep=models.Cards.select(
                            models.Cards.name,
                            models.Cards.text).join(models.MINIONCards).where(  # type: ignore
                                models.Cards.dbfid==models.MINIONCards.Cardid,
                                models.MINIONCards.cost==minion_cost,
                                models.MINIONCards.attack==minion_attack,
                                models.MINIONCards.health==minion_health,
                            )
                        message_str=f"身材为{minion_cost}-{minion_attack}-{minion_health}的随从有:\n"
                        for i,j in enumerate(tep):
                            message_str+=str(i+1)+'. '+j.name+'\n'

                        await cards_query.send(message=message_str)         
                    except:
                        await cards_query.send(message="您的输入有误，请输入“查随从 x-x-x”，例如“查随从 9-3-9”")         
    
    #请求结束，关数据库
    if not models.database.is_closed():
        models.database.close()
