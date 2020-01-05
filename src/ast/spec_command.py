from src.ast.instruction import Instruction
from src.lexer.token import Token


class SpecialCommand(Instruction):

    def __init__(self, token: Token):
        self.command = token.type

    def get_representation(self) -> str:
        return 'Special command: ' + self.command.name

    def get_children(self) -> None:
        return None
