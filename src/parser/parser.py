from src.lexer.lexer import Lexer

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
from src.ast.text import Text

from src.lexer.token import Token
from src.lexer.lex_type import LexType
from typing import Optional, List, Tuple


class Parser:

    def __init__(self, lexer: Lexer):
        self._lexer = lexer
        self._current_token: Optional[Token] = None

    def parse(self) -> ASTNode:
        return self._parse_instruction_block()

    def _consume_token(self) -> Token:
        result = self._current_token
        self._current_token = self._lexer.next_token()
        return result

    def _accept(self, token_types: List[LexType]) -> bool:
        return self._current_token.type in token_types

    def _accept_and_consume_token(self, token_type: LexType):
        if self._accept([token_type]):
            self._consume_token()
        else:
            raise ParserError

    def _parse_instruction_block(self) -> InstructionBlock:
        instructions: List[Instruction] = []
        while self._current_token.type != LexType.eof:
            instructions.append(self._parse_instruction())

        return InstructionBlock(instructions=instructions)

    def _parse_instruction(self) -> Instruction:
        if self._accept([LexType.gamestate_kw, LexType.reset_kw, LexType.clear_cards_kw]):
            return self._parse_spec_command()
        elif self._accept([LexType.object_id]):
            return self._parse_action_or_assignment()
        elif self._accept([LexType.repeat_kw]):
            return self._parse_loop()
        else:
            raise ParserError

    def _parse_spec_command(self) -> SpecialCommand:
        result = SpecialCommand(token=self._current_token)
        self._consume_token()
        return result

    def _parse_action_or_assignment(self) -> Instruction:
        actions = [LexType.block_kw, LexType.attack_kw, LexType.life_kw, LexType.remove_kw, LexType.destroy_kw,
                   LexType.exile_kw, LexType.add_kw, LexType.repeat_kw]

        object: Object = self._parse_object()

        if self._accept([LexType.assign_op]):
            self._consume_token()
            definition: Definition = self._parse_definition()
            return Assignment(object=object, definition=definition)
        elif self._accept(actions):
            action_token: Token = self._consume_token()
            if self._accept([LexType.object_id]):
                object2 = self._parse_object()
            else:
                object2 = None

            return Action(token=action_token, object1=object, object2=object2)
        else:
            raise ParserError

    def _parse_definition(self) -> Definition:
        if self._accept([LexType.func_name]):
            function_name: str = self._consume_token().type.name
        else:
            raise ParserError

        if function_name == 'Player':
            self._accept_and_consume_token(LexType.left_bracket)
            self._accept_and_consume_token(LexType.right_bracket)
            return Definition(func_name=function_name, arguments=[])
        elif function_name == 'Card':
            self._accept_and_consume_token(LexType.left_bracket)
            args = self._parse_arguments(['text', 'text', 'text', 'number', 'number', 'text'])
            self._accept_and_consume_token(LexType.right_bracket)
            return Definition(func_name=function_name, arguments=args)
        elif function_name == 'Token':
            self._accept_and_consume_token(LexType.left_bracket)
            args = self._parse_arguments(['text', 'number', 'number', 'text'])
            self._accept_and_consume_token(LexType.right_bracket)
            return Definition(func_name=function_name, arguments=args)
        elif function_name == 'Property':
            self._accept_and_consume_token(LexType.left_bracket)
            args = self._parse_arguments(['number'])
            self._accept_and_consume_token(LexType.right_bracket)
            return Definition(func_name=function_name, arguments=args)
        else:
            raise ParserError

    def _parse_arguments(self, type_list: List[str]) -> List:
        result = []
        for arg in type_list:
            if arg == 'text':
                if self._accept([LexType.text]):
                    result.append(Text(token=self._consume_token()))
                else:
                    raise ParserError
            elif arg == 'number':
                if self._accept([LexType.number]):
                    result.append(Number(token=self._consume_token()))
                else:
                    raise ParserError
            else:
                raise ParserError

        return result

    def _parse_object(self) -> Object:
        if self._accept([LexType.object_id]):
            part_1: Token = self._consume_token()
        else:
            raise ParserError

        if self._accept([LexType.property_op]):
            part_2: Token = self._consume_token()
            return Object(object=part_1, object_property=part_2, card=None, object_type='property')
        elif self._accept([LexType.card_op]):
            part_2: Token = self._consume_token()
        else:
            return Object(object=part_1, card=None, object_property=None, object_type='player')

        if self._accept([LexType.property_op]):
            part_3: Token = self._consume_token()
            return Object(object=part_1, card=part_2, object_property=part_3, object_type='card_property')
        else:
            return Object(object=part_1, card=part_2, object_property=None, object_type='card')

    def _parse_loop(self) -> Loop:
        self._consume_token()
        if self._accept([LexType.number]):
            token: Token = self._consume_token()
            count: Number = Number(token=token)
        else:
            raise ParserError

        if self._accept([LexType.left_curl_bracket]):
            self._consume_token()
            block: InstructionBlock = self._parse_instruction_block()
        else:
            raise ParserError

        if self._accept([LexType.right_curl_bracket]):
            self._consume_token()
        else:
            raise ParserError

        return Loop(count=count, block=block)


class ParserError(Exception):
    pass
