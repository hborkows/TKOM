from src.objects.card import Card
from typing import Dict


class Player:

    def __init__(self, name: str):
        self.properties: Dict[str: int] = {}
        self.cards: Dict[str: Card] = {}
        self.name = name
        self.add_property(name='life', value=20)

    def add_card(self, card: Card):
        self.cards[card.name] = card

    def remove_card(self, name: str):
        self.cards.pop(name)

    def add_property(self, name: str, value: int):
        self.properties[name] = value

    def get_property_by_name(self, name: str):
        return self.properties[name]
