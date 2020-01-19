from src.parser.parser import Parser
from src.interpreter.symbol_table import SymbolTable

from src.ast.ast_node import ASTNode
from src.ast.ast_node import ASTNode
from src.ast.instruction_block import InstructionBlock
from src.ast.instruction import Instruction
from src.ast.spec_command import SpecialCommand
from src.ast.action import Action
from src.ast.loop import Loop
from src.ast.assignment import Assignment
from src.ast.number import Number
from src.ast.object import Object
from src.ast.definition import Definition
from src.ast.math_expression import MathExpression
from src.ast.math_op import MathOp


class NodeVisitor(object):
    def _visit(self, node: ASTNode):
        method_name = '_visit_' + type(node).__name__
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):

    def __init__(self, parser: Parser, symbol_table: SymbolTable):
        self._parser = parser
        self._symbol_table = symbol_table

    def interpret(self):
        tree: ASTNode = self._parser.parse()
        self._visit(tree)

    def _visit_InstructionBlock(self, node: InstructionBlock):
        for instruction in node.get_children():
            self._visit(instruction)

    def _visit_Instruction(self, node: Instruction):
        if isinstance(node, SpecialCommand):
            self._visit(node)
        elif isinstance(node, Assignment):
            pass
        elif isinstance(node, Action):
            pass
        else:
            raise InterpreterError

    def _visit_SpecialCommand(self, node: SpecialCommand):
        if node.command.name == 'gamestate':
            print('Gamestate:')
            for symbol in self._symbol_table.get_symbols_by_type(symbol_type='any'):
                print(symbol.get_representation())
        elif node.command.name == 'reset':
            self._symbol_table.clear()
            print('Gamestate has been reset.')
        elif node.command.name == 'clear_cards':
            self._symbol_table.remove_symbols_by_type(symbol_type='card')
            print('Cards have been cleared.')
        else:
            raise InterpreterError


class InterpreterError(Exception):
    pass
