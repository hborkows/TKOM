from src.ast.instruction import Instruction
from src.lexer.token import Token
from src.ast.object import Object


class Action(Instruction):

    def __init__(self, object, token: Token):
        self.object =
        self.action_name = token.type

    def get_representation(self) -> str:
        return 'Action: '