from typing import Optional, List
from src.lexer.token import Token
from src.lexer.lex_type import LexType
from src.ast.ast_node import ASTNode


class Object(ASTNode):

    def __init__(self, object_base: Token, object_type: str, object_property: Optional[Token] = None, card: Optional[Token] = None):
        self.id = object_base.text

        if object_property:
            self.property = object_property.text
        else:
            self.property = None

        if card:
            self.card = card.text
        else:
            self.card = None
        self.type = object_type

    def get_representation(self) -> str:
        if self.type == 'player':
            return 'Player: ' + self.id
        elif self.type == 'card':
            return 'Card: ' + self.id + ':' + self.card
        elif self.type == 'card_property':
            return 'Card property: ' + self.id + ':' + self.card + '.' + self.property
        elif self.type == 'property':
            return 'Property: ' + self.id + '.' + self.property

    def get_children(self) -> Optional[List]:
        return []

