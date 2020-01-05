from src.ast.ast_node import ASTNode
from typing import Optional, List
from src.lexer.token import Token


class Number(ASTNode):

    def __init__(self, token: Token):
        self.value = token.number

    def get_representation(self) -> str:
        return 'Number: ' + str(self.value)

    def get_children(self) -> Optional[List]:
        return None
