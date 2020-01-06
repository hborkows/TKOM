from typing import Optional, List
from src.ast.instruction import Instruction
from src.lexer.token import Token
from src.ast.object import Object


class Action(Instruction):

    def __init__(self, token: Token, object1: Object, object2: Optional[Object]):
        self.object1 = object1
        self.object2 = object2
        self.action_name = token.type

    def get_representation(self) -> str:
        return 'Action: ' + self.action_name.name

    def get_children(self) -> Optional[List]:
        return [self.object1, self.object2]
