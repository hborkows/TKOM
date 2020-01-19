from src.parser.parser import Parser
from src.ast.ast_node import ASTNode


class NodeVisitor(object):
    def _visit(self, node: ASTNode):
        method_name = '_visit_' + type(node).__name__
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):

    def __init__(self, parser: Parser):
        self._parser = parser

    def interpret(self):
        tree: ASTNode = self._parser.parse()
        return self._visit(tree)

