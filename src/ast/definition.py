from src.ast.ast_node import ASTNode
from typing import List, Optional


class Definition(ASTNode):

    def __init__(self, func_name: str, arguments: List):
        self.func_name = func_name
        self.arguments = arguments

    def get_representation(self) -> str:
        return 'Definition: ' + self.func_name

    def get_children(self) -> Optional[List]:
        return self.arguments
