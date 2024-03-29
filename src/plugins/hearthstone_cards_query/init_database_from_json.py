from . import models
import json


def init_database_from_json(json_url="./json_file/cards.collectible.json"):
    """读取json文件，更新数据库"""
    fd = open(json_url, "r", encoding="utf8")
    cards_list = json.loads(fd.read())
    fd.close()
    for card in cards_list:
        if 'set' in card and card['set'] != "HERO_SKINS" and card[
                'set'] != "VANILLA":  # 皮肤或者过时的卡牌，不存储
            try:
                text = ""
                if 'text' in card.keys():
                    text = card['text']
                artist = ""
                if 'artist' in card.keys():
                    artist = card['artist']
                flavor = ""
                if 'flavor' in card.keys():
                    flavor = card['flavor']

                models.Cards.create(dbfid=card['dbfId'],
                                    id=card['id'],
                                    name=card['name'],
                                    type=card['type'],
                                    rarity=card['rarity'],
                                    cardClass=card['cardClass'],
                                    set=card['set'],
                                    text=text,
                                    artist=artist,
                                    flavor=flavor)

                if card['type'] == "MINION":
                    race = ""
                    if 'race' in card.keys():
                        race = card['race']
                    models.MINIONCards.create(Cardid=card['dbfId'],
                                              cost=card['cost'],
                                              attack=card['attack'],
                                              health=card['health'],
                                              race=race)

                elif card['type'] == "SPELL":
                    spellSchool = ""
                    if 'spellSchool' in card.keys():
                        spellSchool = card['spellSchool']
                    models.SPELLCards.create(Cardid=card['dbfId'],
                                             cost=card['cost'],
                                             spellSchool=spellSchool)

                elif card['type'] == "HERO":
                    armor = 0
                    if 'armor' in card.keys():
                        armor = card['armor']
                    cost = -1
                    if 'cost' in card.keys():
                        cost = card['cost']
                    models.HEROCards.create(
                        Cardid=card['dbfId'],
                        cost=cost,
                        armor=armor,
                        health=card['health'],
                    )

                elif card['type'] == "WEAPON":
                    models.WEAPONCards.create(Cardid=card['dbfId'],
                                              cost=card['cost'],
                                              attack=card['attack'],
                                              durability=card['durability'])

                elif card['type'] == "LOCATION":
                    models.LOCATIONCards.create(Cardid=card['dbfId'],
                                                cost=card['cost'],
                                                health=card['health'])
            except Exception as e:
                print(repr(e))
                print(card)
