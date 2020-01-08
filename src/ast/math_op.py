from src.ast.ast_node import ASTNode
from src.lexer.token import Token
from typing import Optional, List


class MathOp(ASTNode):

    def __init__(self, token: Token):
        self.operator = token.type

    def get_representation(self) -> str:
        return self.operator.name

    def get_children(self) -> Optional[List]:
        return []
