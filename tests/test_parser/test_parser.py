import unittest
from typing import List

from src.parser.parser import Parser
from src.lexer.lexer import Lexer
from src.source.source import Source
from src.lexer.token import Token
from src.lexer.lex_type import LexType

from src.ast.instruction_block import InstructionBlock
from src.ast.spec_command import SpecialCommand
from src.ast.assignment import Assignment
from src.ast.definition import Definition
from src.ast.object import Object
from src.ast.math_expression import MathExpression
from src.ast.number import Number
from src.ast.math_op import MathOp
from src.ast.ast_node import ASTNode
from src.ast.action import Action


def print_ast(root: ASTNode, log: List[str]):
    if root:
        for child in root.get_children():
            print_ast(child, log)
        log.append(root.get_representation())


class TestParser(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = Parser(lexer=Lexer(source=Source()))

    def test_special_command(self):
        self.parser.get_lexer().get_source().set_code_line('gamestate')
        node = self.parser.parse()
        test_node = InstructionBlock(instructions=[SpecialCommand(token=Token(lex_type=LexType.gamestate_kw))])

        self.assertEqual(node.get_children()[0].get_representation(), test_node.get_children()[0].get_representation())

    def test_assignment_player(self):
        self.parser.get_lexer().get_source().set_code_line('hubert = Player()')
        node = self.parser.parse()

        test_node = InstructionBlock(instructions=[
            Assignment(
                object=Object(object_base=Token(lex_type=LexType.object_id, text='hubert'), object_type='player'),
                definition=Definition(func_name='Player', arguments=[]))])

        obj_type = node.get_children()[0].get_children()[0].get_representation()
        func_name = node.get_children()[0].get_children()[1].get_representation()

        test_obj_type = test_node.get_children()[0].get_children()[0].get_representation()
        test_func_name = test_node.get_children()[0].get_children()[1].get_representation()

        self.assertEqual(obj_type, test_obj_type)
        self.assertEqual(func_name, test_func_name)

    def test_assignment_property(self):
        self.parser.get_lexer().get_source().set_code_line('hubert.health = Property(2 * 2 + 1)')
        node = self.parser.parse()

        test_arg = MathExpression(operand1=MathExpression(operand1=Number(Token(LexType.number, number=2)),
                                                          operand2=Number(Token(LexType.number, number=2)),
                                                          operator=MathOp(token=Token(LexType.mul_op))),
                                  operand2=Number(Token(LexType.number, number=1)),
                                  operator=MathOp(Token(LexType.add_op)))

        test_node = InstructionBlock(instructions=[
            Assignment(object=Object(object_base=Token(lex_type=LexType.object_id, text='hubert'),
                                     object_type='property',
                                     object_property=Token(lex_type=LexType.object_id, text='health')),
                       definition=Definition(func_name='Property', arguments=[test_arg]))
        ])

        node_log = []
        test_log = []
        print_ast(node, node_log)
        print_ast(test_node, test_log)

        self.assertEqual(node_log, test_log)

    def test_action(self):
        self.parser.get_lexer().get_source().set_code_line('hubert:bear attack janek:construct')
        node = self.parser.parse()

        test_node = InstructionBlock(instructions=[
            Action(token=Token(LexType.attack_kw),
                   object1=Object(object_base=Token(lex_type=LexType.object_id, text='hubert'),
                                  object_type='card',
                                  card=Token(LexType.object_id, text='bear')),
                   object2=Object(object_base=Token(lex_type=LexType.object_id, text='janek'),
                                  object_type='card',
                                  card=Token(LexType.object_id, text='construct')))
        ])

        node_log = []
        test_log = []
        print_ast(node, node_log)
        print_ast(test_node, test_log)

        self.assertEqual(node_log, test_log)
