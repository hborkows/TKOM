from src.ast.ast_node import ASTNode
from src.ast.instruction_block import InstructionBlock
from src.ast.math_expression import MathExpression
from typing import Optional, List


class Loop(ASTNode):

    def __init__(self, count: MathExpression, block: InstructionBlock):
        self.block = block
        self.count = count

    def get_representation(self) -> str:
        return 'Loop'

    def get_children(self) -> Optional[List]:
        return [self.count, self.block]
