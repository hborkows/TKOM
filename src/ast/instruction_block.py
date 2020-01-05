from typing import List
from src.ast.ast_node import ASTNode
from src.ast.instruction import Instruction


class InstructionBlock(ASTNode):

    def __init__(self, instructions: List[Instruction]):
        self.instructions = instructions

    def get_representation(self) -> str:
        return 'Instruction Block ( ' + str(len(self.instructions)) + ' instructions)'

    def get_children(self) -> List[ASTNode]:
        return self.instructions
