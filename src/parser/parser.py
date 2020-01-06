from src.lexer.lexer import Lexer
from src.ast.ast_node import ASTNode
from src.lexer.token import Token
from src.lexer.lex_type import LexType
from typing import Optional, List, Tuple


class Parser:

    def __init__(self, lexer: Lexer):
        self._lexer = lexer
        self._current_token: Optional[Token] = None

    def parse(self) -> ASTNode:
        pass

    def _consume_token(self) -> Token:
        result = self._current_token
        self._current_token = self._lexer.next_token()
        return result

    def _accept(self, token_types: Tuple[LexType]) -> bool:
        return self._current_token.type in token_types

    def _parse_instruction_block(self):