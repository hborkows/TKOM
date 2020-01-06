from src.ast.ast_node import ASTNode
from src.ast.math_op import MathOp
from typing import Optional, List
from src.lexer.token import Token


class MathExpression(ASTNode):

    def __init__(self, operand1: ASTNode, operand2: ASTNode, operator: MathOp):
        self.operand1 = operand1
        self.operand2 = operand2
        self.operator = operator

    def get_representation(self) -> str:
        if self.operator:
            return 'Expression: '
        else:
            return "Number: " + self.operand1.get_representation()

    def get_children(self) -> Optional[List]:
        result: List[ASTNode] = []
        if self.operand1:
            result.append(self.operand1)
        if self.operator:
            result.append(self.operator)
        if self.operand2:
            result.append(self.operand2)
        return result
