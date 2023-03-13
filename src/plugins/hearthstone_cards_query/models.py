from .config import DATABASE_NAME, DATABASE_PASSWORD, DATABASE_CHARSET, DATABASE_HOST, DATABASE_PORT, DATABASE_USER
import peewee as pw
# py_peewee连接的数据库名
#数据库得自己建立，peewee只有建立数据表的权限
database = pw.MySQLDatabase(DATABASE_NAME,
                            host=DATABASE_HOST,
                            user=DATABASE_USER,
                            passwd=DATABASE_PASSWORD,
                            charset=DATABASE_CHARSET,
                            port=DATABASE_PORT)


class BaseModel(pw.Model):

    class Meta:
        database = database  # 将实体与数据库进行绑定


class Cards(BaseModel):
    dbfid = pw.IntegerField(primary_key=True, null=False, unique=True,
                            index=True)  #构造及解析卡牌代码的数值,dbfId
    id = pw.CharField(max_length=32, null=False, unique=True)  # 卡牌的字符串标识
    name = pw.CharField(max_length=32, null=False, index=True)
    #随从牌、法术牌、英雄牌、武器牌、地标
    type = pw.CharField(
        max_length=32
        #constraints=[pw.Check('type in ("MINION", "SPELL", "HERO","WEAPON","LOCATION")')]
    )
    #普通、稀有、史诗、传说、免费
    rarity = pw.CharField(
        max_length=32,
        null=False
        #constraints=[pw.Check('rarity in ("COMMON", "RARE", "EPIC", "LEGENDARY","FREE")')]
    )
    #中立及十职业
    cardClass = pw.CharField(
        max_length=32,
        null=False
        #constraints=[
        #    pw.Check(
        #        'cardClass in ("MAGE", "HUNTER", "PRIEST", "NEUTRAL", "WARLOCK", "ROGUE", "DRUID", "SHAMAN", "WARRIOR", "PALADIN", "DEMONHUNTER")'
        #    )
        #]
    )
    set = pw.CharField(max_length=32)  #来自哪个系列或拓展包
    text = pw.CharField(max_length=1024)  #卡牌描述
    artist = pw.CharField(max_length=255)  #画师
    flavor = pw.CharField(max_length=2048)  #卡牌趣闻

    def __repr__(self):
        return '<Cards {}{}>'.format(self.name)


class MINIONCards(BaseModel):
    Cardid = pw.ForeignKeyField(Cards, primary_key=True, null=False, unique=True, index=True)
    cost = pw.IntegerField(null=False)  #法力值消耗(费用)
    attack = pw.IntegerField(null=False, constraints=[pw.Check('attack >= 0')])
    health = pw.IntegerField(null=False, constraints=[pw.Check('health >= 0')])
    #随从种族，可为空
    #龙、恶魔、海盗、野兽、图腾、鱼人、元素、机械、野猪人、娜迦、全部
    race = pw.CharField(
        max_length=32
        #constraints=[
        #    pw.Check(
        #        'race in ("","NAGA","DRAGON", "DEMON", "PIRATE", "BEAST", "TOTEM", "MURLOC", "ELEMENTAL", "MECHANICAL", "QUILBOAR", "ALL")'
        #    )
        #]
    )


class SPELLCards(BaseModel):
    Cardid = pw.ForeignKeyField(Cards, primary_key=True, null=False, unique=True, index=True)
    cost = pw.IntegerField(null=False)  #法力值消耗(费用)

    #法术派系，可为空
    #火焰、奥术、神圣、暗影、邪能、自然、冰霜
    spellSchool = pw.CharField(
        max_length=32
        #constraints=[
        #    pw.Check(
        #        'spellSchool in ("","FIRE", "ARCANE", "HOLY", "SHADOW", "FEL", "NATURE", "FROST")')
        #]
    )


class HEROCards(BaseModel):
    Cardid = pw.ForeignKeyField(Cards, primary_key=True, null=False, unique=True, index=True)
    cost = pw.IntegerField()  #法力值消耗(费用)
    armor = pw.IntegerField()  #护甲
    health = pw.IntegerField()  #生命


class WEAPONCards(BaseModel):
    Cardid = pw.ForeignKeyField(Cards, primary_key=True, null=False, unique=True, index=True)
    cost = pw.IntegerField(null=False)  #法力值消耗(费用)
    attack = pw.IntegerField(null=False, constraints=[pw.Check('attack >= 0')])
    #耐久度
    durability = pw.IntegerField(null=False, constraints=[pw.Check('durability >= 0')])


class LOCATIONCards(BaseModel):
    Cardid = pw.ForeignKeyField(Cards, primary_key=True, null=False, unique=True, index=True)
    cost = pw.IntegerField(null=False)  #法力值消耗(费用)
    health = pw.IntegerField()  #生命
