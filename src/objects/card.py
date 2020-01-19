from typing import Dict


class Card:

    def __init__(self, name: str):
        self.properties: Dict[str: int] = {}
        self.name = name

    def add_property(self, name: str, value: int):
        self.properties[name] = value
