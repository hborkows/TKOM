from typing import Dict


class Card:

    def __init__(self, name: str, card_name: str, card_type: str, power: int, toughness: int, rest: str = ''):
        self.properties: Dict[str: int] = {}
        self.name = name,
        self.card_name = card_name
        self.card_type = card_type
        self.rest = rest
        self.add_property('power', power)
        self.add_property('toughness', toughness)

    def add_property(self, name: str, value: int):
        self.properties[name] = value

    def get_property_by_name(self, name: str):
        if name in self.properties.keys():
            return self.properties[name]
        else:
            return None

    def get_representation(self):
        result = '\n'
        for key in self.properties.keys():
            result += '---' + key + ': ' + str(self.properties[key]) + '\n'

        return result
