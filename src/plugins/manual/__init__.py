
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

manual=on_command("man",aliases={"manual","使用手册","手册","指令"},priority=1,block=True)

@manual.handle()
async def _(bot:Bot,event:MessageEvent):
    message_str="HSBot 使用手册\n"
    message_str+="1. jjc选牌助手 指令: \njjc选牌 <职业> [卡牌列表]\n例: jjc选牌 德 团本 哥利亚 伊瑟拉\n"
    message_str+="\n2. jjc奥秘提示 指令: \njjc猜奥秘 <职业>\n例: jjc猜奥秘 骑士\n"
    message_str+="\n3. 卡牌查询 指令: \n查卡牌 <卡牌规则>\n查随从 <随从身材>\n例: 查随从 9-3-9\n"
    message_str+="\n4. 胜率查询 指令: \n查胜率 <标准/狂野/jjc/对决/经典>\n例: 查胜率 jjc\n"
    message_str+="\n5. 榜单查询 指令: \n<查标准/狂野/酒馆/经典/佣兵> <你要搜索的串>\n例: 查标准 济往\n"
    message_str+="\n6. 每日早报 指令: \n<早报/今日早报/60s/60秒早报>"
    message_str+="\n7. 抽签 指令: \n<抽签/今日运势/运势>"
    await manual.send(message=message_str)