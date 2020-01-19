from src.ast.object import Object


class Symbol:

    def __init__(self, name: str, symbol_type: str, value: int, base_object: Object, parent):
        self.name = name
        self.symbol_type = symbol_type
        self.value = value
        self.base_object = base_object
        self.parent = parent

    def get_representation(self):
        return self.base_object.get_representation()

    def get_children(self):
        return self.base_object.get_children()
