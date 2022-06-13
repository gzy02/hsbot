#管理员才有权限的操作
from .utility import verify_admin,connect_and_close_database
from . import reset_database
from . import models
from . import init_database_from_json
from . import ask_json
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

@reset_database.handle()
@connect_and_close_database
@verify_admin(Matcher=reset_database)#必须是管理员才行
async def _reset_database(bot: Bot, event: MessageEvent):
    await reset_database.send(message="开始重置...")

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
    await reset_database.send(message="重置完成")
