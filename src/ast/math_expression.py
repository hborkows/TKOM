from src.ast.ast_node import ASTNode
from typing import Optional, List
from src.lexer.token import Token


class MathExpression(ASTNode):

    def __init__(self, operand1: ASTNode, operand2: ASTNode, operator: Token):
        self.operand1 = operand1
        self.operand2 = operand2
        self.operator = operator.type

    def get_representation(self) -> str:
        if self.operator:
            return 'Expression: ' + self.operator.name
        else:
            return "Number: " + self.operand1.get_representation()

    def get_children(self) -> Optional[List]:
        result: List[ASTNode] = []
        if self.operand1:
            result.append(self.operand1)
        if self.operand2:
            result.append(self.operand2)
        return result
