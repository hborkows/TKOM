from typing import List
from src.ast.ast_node import ASTNode
from src.ast.instruction import Instruction


class InstructionBlock(ASTNode):

    def __init__(self, instructions: List[Instruction]):
        self._instructions = instructions

    def print(self):
        for instruction in self._instructions:
            instruction.print()
