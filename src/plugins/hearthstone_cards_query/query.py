from . import models
import peewee


def find_minion_by_body(minion_cost, minion_attack, minion_health) -> str:
    tep = models.Cards.select(models.Cards.name,
                              models.Cards.text).join(models.MINIONCards).where(  # type: ignore
                                  models.Cards.dbfid == models.MINIONCards.Cardid,
                                  models.MINIONCards.cost == minion_cost,
                                  models.MINIONCards.attack == minion_attack,
                                  models.MINIONCards.health == minion_health)
    message_str = f"身材为{minion_cost}-{minion_attack}-{minion_health}的随从有:\n"
    for i, j in enumerate(tep):
        message_str += str(i + 1) + '. ' + j.name + '\n'
    return message_str


def find_card_by_text(text: str) -> peewee.ModelSelect:
    return models.Cards.select(models.Cards.name, models.Cards.cardClass, models.Cards.dbfid,
                               models.Cards.id, models.Cards.text, models.Cards.set).where(
                                   (models.Cards.name.contains(text)
                                    | models.Cards.text.contains(text)))


def find_card_by_name(name: str) -> peewee.ModelSelect:
    return models.Cards.select(models.Cards.name, models.Cards.cardClass, models.Cards.dbfid,
                               models.Cards.id, models.Cards.text, models.Cards.set).where(
                                   (models.Cards.name.contains(name)))


def find_all_set() -> peewee.ModelSelect:
    return models.Cards.select(models.Cards.set).distinct()