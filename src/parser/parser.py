from src.lexer.lexer import Lexer

from src.ast.ast_node import ASTNode
from src.ast.instruction_block import InstructionBlock
from src.ast.instruction import Instruction
from src.ast.spec_command import SpecialCommand
from src.ast.action import Action
from src.ast.loop import Loop
from src.ast.assignment import Assignment
from src.ast.number import Number

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

    def _parse_action_or_assignment(self) -> Action:
        pass

    def _parse_assignment(self) -> Assignment:
        pass

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
