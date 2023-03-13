from nonebot import on_command, on_fullmatch
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from time import sleep

manual = on_fullmatch(msg=("manual", "使用手册", "手册", "指令", "man"), priority=1, block=True)


@manual.handle()
async def _manual(bot: Bot, event: MessageEvent):
    """使用手册"""
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
    if event.message_type == "group":
        message_str = f'[CQ:at,qq={event.get_user_id()}]' + message_str
    await manual.send(message=Message(message_str))

    sleep(3)

    message_str = "HSBot 使用手册(管理员)"
    message_str += "\n11.查系列(游戏更新时管理员可以用此指令查询新系列在数据库中的名字) 指令: \n查系列/查询所有系列"
    message_str += "\n12.重置jjc环境(游戏更新时管理员可以用此指令重置jjc环境) 指令: \n<重置jjc/重置jjc系列/重置jjc环境> <新的jjc系列列表>\n例: 重置jjc CORE BOOMSDAY DRAGONS THE_BARRENS STORMWIND THE_SUNKEN_CITY ALTERAC_VALLEY"

    message_str += "\n13.查系列jjc(游戏更新时管理员可以用此指令查询jjc是否将新系列设置成功) 指令: \n查系列jjc"
    message_str += "\n14.重置数据库(游戏更新时管理员可以用此指令更新新的卡包) 指令: \n重置数据库"
    message_str += "\n15.查询管理员 指令: \n查询管理员/管理员查询"
    message_str += "\n16.添加管理员(管理员可以用此指令添加新的管理员) 指令: \n添加管理员 <管理员qq号>"
    message_str += "\n17.删除管理员(系统管理员可以用此指令删除管理员) 指令: \n删除管理员 <管理员qq号>"

    if event.message_type == "group":
        message_str = f'[CQ:at,qq={event.get_user_id()}]' + message_str
    await manual.send(message=Message(message_str))
    sleep(3)
    
    message_str="ChatGPT使用手册\n使用前请注意：1.单次连续会话只允许4096token，约3000字。因此，达到一定阈值后bot将自动重置你的会话，请在合理时机自行重置会话\n2.为了防止qq群刷屏，单次请求至多1000字\n3.不支持图片、Emoji，请勿在请求中加入这类无关字符\n4.该bot已设置为允许加好友，私聊模式下第二个限制予以解除，但第一个限制仍然存在\n功能列表：\n0.#GPT设定 <你要说的话>\n例：#GPT设定 你现在是游戏《炉石传说》设计师\n更多设定可参考https://github.com/PlexPt/awesome-chatgpt-prompts-zh\n1.#GPT <你要说的话>\n例: #GPT 设计一张1费德鲁伊法术，效果要强\n2.重置会话"

    if event.message_type == "group":
        message_str = f'[CQ:at,qq={event.get_user_id()}]' + message_str
    await manual.send(message=Message(message_str))
