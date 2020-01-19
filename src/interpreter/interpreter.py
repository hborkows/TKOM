from src.parser.parser import Parser
from src.interpreter.symbol_table import SymbolTable, Symbol

from src.ast.ast_node import ASTNode
from src.ast.instruction_block import InstructionBlock
from src.ast.instruction import Instruction
from src.ast.spec_command import SpecialCommand
from src.ast.action import Action
from src.ast.loop import Loop
from src.ast.assignment import Assignment
from src.ast.number import Number
from src.ast.object import Object
from src.ast.math_expression import MathExpression
from src.lexer.lex_type import LexType

from src.objects.card import Card
from src.objects.player import Player


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
        self._symbol_table = SymbolTable()

    def interpret(self):
        tree: ASTNode = self._parser.parse()
        self._visit(tree)

    def _visit_InstructionBlock(self, node: InstructionBlock):
        for instruction in node.get_children():
            self._visit(instruction)

    def _visit_Instruction(self, node: Instruction):
        if isinstance(node, SpecialCommand) or isinstance(node, Assignment) or isinstance(node, Action) or isinstance(node, Loop):
            self._visit(node)
        else:
            raise InterpreterError

    def _visit_SpecialCommand(self, node: SpecialCommand):
        if node.command == LexType.gamestate_kw:
            print('Gamestate:')
            for symbol in self._symbol_table.get_symbols_by_type(symbol_type='any'):
                print(symbol.get_representation())
        elif node.command == LexType.reset_kw:
            self._symbol_table.clear()
            print('Gamestate has been reset.')
        elif node.command == LexType.clear_cards_kw:
            self._symbol_table.remove_symbols_by_type(symbol_type='card')
            print('Cards have been cleared.')
        else:
            raise InterpreterError

    def _visit_Action(self, node: Action):
        if not self._symbol_table.is_symbol_defined(node.object1.get_name()):
            raise InterpreterError

        if node.action_name in (LexType.destroy_kw, LexType.remove_kw, LexType.exile_kw):
            if not self._symbol_table.get_symbol_by_name(name=node.object1.get_name()).symbol_type == 'card':
                raise InterpreterError
            self._symbol_table.remove_symbol_by_name(name=node.object1.get_name())

        elif node.action_name in (LexType.inc_op, LexType.dec_op):
            if not self._symbol_table.get_symbol_by_name(name=node.object1.get_name()).symbol_type in ('property', 'card_property'):
                raise InterpreterError

            cur_property = self._symbol_table.get_symbol_by_name(name=node.object1.get_name()).parent.value.get_property_by_name(name=node.object1.get_property())

            if node.action_name == LexType.inc_op:
                cur_property += 1
            else:
                cur_property += 1

        elif node.action_name == LexType.block_kw:
            pass

        elif node.action_name == LexType.attack_kw:
            if not self._symbol_table.is_symbol_defined(node.object2.get_name()):
                raise InterpreterError

            card1 = self._symbol_table.get_symbol_by_name(name=node.object1.get_name())
            card2 = self._symbol_table.get_symbol_by_name(name=node.object2.get_name())

            if card1.symbol_type != 'card' or card2.symbol_type != 'card':
                raise InterpreterError

            card1_death = False
            card2_death = False

            if card1.value.get_property_by_name(name='power') > card2.value.get_property_by_name(name='toughness'):
                card2_death = True
            if card2.value.get_property_by_name(name='power') > card1.value.get_property_by_name(name='toughness'):
                card1_death = True

            if card1_death:
                self._symbol_table.remove_symbol_by_name(card1.name)
            if card2_death:
                self._symbol_table.remove_symbol_by_name(card2.name)

    def _visit_Assignment(self, node: Assignment):
        # Handle object name
        cur_object = node.get_children()[0]
        self._visit(cur_object)

        # Handle value
        definition = node.get_children()[1]

        if definition.func_name == 'Player':
            if cur_object.get_type() != 'player':
                raise InterpreterError
            self._symbol_table.get_symbol_by_name(name=cur_object.get_id()).value = Player(name=cur_object.get_id())
        elif definition.func_name == 'Card':
            if cur_object.get_type() != 'card':
                raise InterpreterError
            name: str = cur_object.get_id() + ':' + cur_object.get_card()
            new_card = Card(name=name, card_name=definition.arguments[0], card_type=definition.arguments[1],
                            power=self._visit(definition.arguments[2]), toughness=self._visit(definition.arguments[3]),
                            rest=definition.arguments[4])
            self._symbol_table.get_symbol_by_name(name=name).value = new_card
            self._symbol_table.get_symbol_by_name(name=cur_object.get_id()).value.add_card(card=new_card)
        elif definition.func_name == 'Token':
            if cur_object.get_type() != 'card':
                raise InterpreterError

            name = cur_object.get_id() + ':' + cur_object.get_card()
            new_card = Card(name=name, card_name='Token', card_type=definition.arguments[1],
                            power=self._visit(definition.arguments[2]), toughness=self._visit(definition.arguments[3]),
                            rest=definition.arguments[4])
            self._symbol_table.get_symbol_by_name(name=name).value = new_card
            self._symbol_table.get_symbol_by_name(name=cur_object.get_id()).value.add_card(card=new_card)
        elif definition.func_name == 'Property':
            if cur_object.get_type() != 'property' and cur_object.get_type() != 'card_property':
                raise InterpreterError
            elif cur_object.get_type() == 'card_property':
                name = cur_object.get_property()
                card_name = cur_object.get_id() + ':' + cur_object.get_card()
                self._symbol_table.get_symbol_by_name(name=card_name).value.add_property(name=name,
                                                                                         value=self._visit(definition.arguments[0]))
            else:
                name = cur_object.get_property()
                player_name = cur_object.get_id()
                self._symbol_table.get_symbol_by_name(name=player_name).value.add_property(name=name,
                                                                                           value=self._visit(definition.arguments[0]))
        else:
            raise InterpreterError

    def _visit_Object(self, cur_object: Object):
        if cur_object.get_type() == 'player':
            if self._symbol_table.is_symbol_defined(name=cur_object.get_id()):
                raise InterpreterError
            self._symbol_table.add_symbol(symbol=Symbol(name=cur_object.get_id(), symbol_type=cur_object.get_type(),
                                                        base_object=cur_object, parent=None,
                                                        value=None))
        elif cur_object.get_type() == 'card':
            if not self._symbol_table.get_symbol_by_name(name=cur_object.get_id()):
                raise InterpreterError
            name = cur_object.get_id() + ':' + cur_object.get_card()
            if self._symbol_table.is_symbol_defined(name=name):
                raise InterpreterError
            self._symbol_table.add_symbol(symbol=Symbol(name=name,
                                                        symbol_type=cur_object.get_type(), base_object=cur_object,
                                                        parent=self._symbol_table.get_symbol_by_name(
                                                            cur_object.get_id()),
                                                        value=None))
        elif cur_object.get_type() == 'card_property':
            if not self._symbol_table.get_symbol_by_name(name=cur_object.get_id()):
                raise InterpreterError
            if not self._symbol_table.get_symbol_by_name(name=cur_object.get_id() + ':' + cur_object.get_card()):
                raise InterpreterError

            name = cur_object.get_id() + ':' + cur_object.get_card() + '.' + cur_object.get_property()
            if self._symbol_table.is_symbol_defined(name=name):
                raise InterpreterError
            parent = self._symbol_table.get_symbol_by_name(cur_object.get_id() + ':' + cur_object.get_card())

            self._symbol_table.add_symbol(symbol=Symbol(name=name, symbol_type=cur_object.get_type(),
                                                        base_object=cur_object,
                                                        parent=parent,
                                                        value=None))
            parent.value.add_property(cur_object.get_property(), 0)
        else:  # player property
            if not self._symbol_table.get_symbol_by_name(name=cur_object.get_id()):
                raise InterpreterError

            name = cur_object.get_id() + '.' + cur_object.get_property()
            if self._symbol_table.is_symbol_defined(name=name):
                raise InterpreterError
            parent = self._symbol_table.get_symbol_by_name(cur_object.get_id())
            self._symbol_table.add_symbol(symbol=Symbol(name=name,
                                                        symbol_type=cur_object.get_type(), base_object=cur_object,
                                                        parent=parent,
                                                        value=None))

    def _visit_MathExpression(self, node: MathExpression) -> int:
        operator = node.operator.operator
        if operator == LexType.add_op:
            return self._visit(node.operand1) + self._visit(node.operand2)
        elif operator == LexType.sub_op:
            return self._visit(node.operand1) - self._visit(node.operand2)
        elif operator == LexType.mul_op:
            return self._visit(node.operand1) * self._visit(node.operand2)
        elif operator == LexType.div_op:
            if self._visit(node.operand2) == 0:
                raise ZeroDivisionError
            return self._visit(node.operand1) / self._visit(node.operand2)

    def _visit_Number(self, node: Number) -> int:
        return node.value

    def _visit_Loop(self, node: Loop):
        repeat_count = self._visit(node.count)
        i = 0
        while i < repeat_count:
            self._visit(node.block)
            i += 1


class InterpreterError(Exception):
    pass
