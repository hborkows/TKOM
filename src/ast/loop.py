from src.ast.ast_node import ASTNode
from src.ast.instruction import Instruction
from src.ast.instruction_block import InstructionBlock
from src.ast.number import Number
from typing import Optional, List


class Loop(Instruction):

    def __init__(self, count: Number, block: InstructionBlock):
        self.block = block
        self.count = count

    def get_representation(self) -> str:
        return 'Loop'

    def get_children(self) -> Optional[List]:
        return [self.count, self.block]
