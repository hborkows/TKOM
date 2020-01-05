from typing import Optional, List
from src.lexer.token import Token
from src.lexer.lex_type import LexType
from src.ast.ast_node import ASTNode


class Object(ASTNode):

    def __init__(self, token: Token, object_property: Optional[ASTNode], card: Optional[ASTNode], type: str):
        self.id = token.text
        self.property = object_property
        self.card = card
        self.type = type

    def get_representation(self) -> str:
        if self.type == 'player':
            return 'Player: ' + self.id
        elif self.type == 'card':
            return 'Card: ' + self.id
        else:
            return 'Property: ' + self.id

    def get_children(self) -> Optional[List]:
        result: List[ASTNode] = []
        if self.card:
            result.append(self.card)
        if self.property:
            result.append(self.property)

        return result

