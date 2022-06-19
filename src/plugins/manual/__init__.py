
from nonebot import on_command,on_fullmatch
from nonebot.adapters.onebot.v11 import Bot, MessageEvent,Message
from time import sleep
manual = on_fullmatch(
    msg=("manual", "使用手册", "手册", "指令","man"), priority=1, block=True)


@manual.handle()
async def _manual(bot: Bot, event: MessageEvent):
    """使用手册"""
    #sleep(1)
    #await manual.send("HSBot 使用手册")
    #sleep(1)
    #await manual.send("1. jjc选牌助手 指令: \n<jjc/jjc选牌/选牌/竞技场选牌> <职业名/全职业> [卡牌列表]\n例: jjc选牌 德 团本 哥利亚 伊瑟拉")
    #sleep(1)
    #await manual.send("2. jjc奥秘提示 指令: \n<jjc猜奥秘/jjc查奥秘/jjc奥秘> <职业名>\n例: jjc猜奥秘 骑士")
    #sleep(1)
    #await manual.send("3. 卡牌查询 指令: \n查卡牌 <卡牌规则>\n查随从 <随从身材>\n例: 查随从 9-3-9")
    #sleep(1)
    #await manual.send("4. 胜率查询 指令: \n查胜率 <标准/狂野/jjc/对决/经典>\n例: 查胜率 jjc")
    #sleep(1)
    #await manual.send("5. 榜单查询 指令: \n<查标准/狂野/酒馆/经典/佣兵> <你要搜索的串>\n例: 查标准 济往")
    #sleep(1)
    #await manual.send("6. 每日早报 指令: \n<早报/今日早报/60s/60秒早报>\n例: 早报")
    #sleep(1)
    #await manual.send("7. 抽签 指令: \n<抽签/今日运势/运势>\n例: 抽签")
    #sleep(1)
    #await manual.send("8. 繁简转化 指令: \n<djwcb/生僻字转换/djw> <要转换的串>\n例: djw 戴佳伟菜逼")
    #sleep(1)
    #await manual.send("9. 卡图查询 指令: \n<查卡图/查图片/查牌面/查卡面/查描述> [卡牌列表]\n例: 查卡图 骑士队长")
    #sleep(1)
    #await manual.send("10.卡组图片生成 \n无指令，收到信息后判断是否为炉石卡组，自动生成图片")
    #sleep(1)
    #await manual.send("11.重置数据库(游戏更新时管理员可以用此指令) 指令: \n重置数据库")
    
    message_str = "HSBot 使用手册"
    message_str += "\n1. jjc选牌助手 指令: \n<jjc/jjc选牌/选牌/竞技场选牌> <职业名/全职业> [卡牌列表]\n例: jjc选牌 德 团本 哥利亚 伊瑟拉"
    message_str += "\n2. jjc奥秘提示 指令: \n<jjc猜奥秘/jjc查奥秘/jjc奥秘> <职业名>\n例: jjc猜奥秘 骑士"
    message_str += "\n3. 卡牌查询 指令: \n查卡牌 <卡牌规则>\n查随从 <随从身材>\n例: 查随从 9-3-9"
    message_str += "\n4. 胜率查询 指令: \n查胜率 <标准/狂野/jjc/对决/经典>\n例: 查胜率 jjc"
    message_str += "\n5. 榜单查询 指令: \n<查标准/狂野/酒馆/经典/佣兵> <你要搜索的串>\n例: 查标准 济往"
    message_str += "\n6. 每日早报 指令: \n<早报/今日早报/60s/60秒早报>\n例: 早报"
    message_str += "\n7. 抽签 指令: \n<抽签/今日运势/运势>\n例: 抽签"
    message_str += "\n8. 繁简转化 指令: \n<djwcb/生僻字转换/djw> <要转换的串>\n例: djw 戴佳伟菜逼"
    message_str += "\n9. 卡图查询 指令: \n<查卡图/查图片/查牌面/查卡面/查描述> [卡牌列表]\n例: 查卡图 骑士队长"
    message_str += "\n10.卡组图片生成 \n无指令，收到信息后判断是否为炉石卡组，自动生成图片"
    message_str += "\n11.重置数据库(游戏更新时管理员可以用此指令) 指令: \n重置数据库"
    if event.message_type=="group":
        message_str=f'[CQ:at,qq={event.get_user_id()}]'+message_str
    await manual.send(message=Message(message_str))
    