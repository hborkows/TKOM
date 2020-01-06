from src.ast.ast_node import ASTNode
from src.lexer.token import Token


class Text(ASTNode):

    def __init__(self, token: Token):
        self.text = token.text

    def get_representation(self) -> str:
        return 'Text: ' + self.text

    def get_children(self) -> Optional[List]:
        return None
