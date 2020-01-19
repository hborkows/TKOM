from typing import Optional
from typing import Tuple
from typing import Dict
from src.lexer.token import Token
from src.source.source import Source
from src.lexer.lex_type import LexType


class LexerError(Exception):
    pass


class Lexer:

    def __init__(self, source: Source):
        self._source = source

    def get_source(self):
        return self._source

    def next_token(self) -> Token:
        self._skip_whitespace()

        token: Token = self._check_keyword()
        if token:
            return token

        token = self._check_number()
        if token:
            return token

        token = self._check_text()
        if token:
            return token

        token = self._check_inc_dec_operator()
        if token:
            return token

        try:
            token = self._check_one_char_symbols()
            return token
        except LexerError:
            raise LexerError

    def _skip_whitespace(self):
        while self._source.get_char().isspace() or self._source.get_char() == ',':
            self._source.pop_char()

    def _check_keyword(self) -> Optional[Token]:
        keywords: Dict[str, LexType] = {
            'gamestate': LexType.gamestate_kw,
            'reset': LexType.reset_kw,
            'clear_cards': LexType.clear_cards_kw,
            'block': LexType.block_kw,
            'attack': LexType.attack_kw,
            'life': LexType.life_kw,
            'remove': LexType.remove_kw,
            'destroy': LexType.destroy_kw,
            'exile': LexType.exile_kw,
            'add': LexType.add_kw,
            'repeat': LexType.repeat_kw,
            'power': LexType.power_kw,
            'toughness': LexType.toughness_kw
        }
        functions: Tuple[str, str, str, str] = ('Player', 'Card', 'Token', 'Property')
        buffer: str = ''

        if self._source.get_char().isalpha():
            buffer += self._source.pop_char()

            while self._source.get_char().isalnum() or self._source.get_char() == '_' or self._source.get_char() == '-':
                buffer += self._source.pop_char()

            if buffer in keywords.keys():  # buffer contains a keyword
                return Token(lex_type=keywords[buffer])
            elif buffer in functions:  # buffer contains an id of function
                return Token(lex_type=LexType.func_name, text=buffer)
            else:  # buffer contains an object id
                return Token(lex_type=LexType.object_id, text=buffer)
        else:
            return None

    def _check_number(self) -> Optional[Token]:
        buffer: str = ''

        if self._source.get_char().isdigit():
            buffer += self._source.pop_char()

            while self._source.get_char().isdigit():
                buffer += self._source.pop_char()

            return Token(LexType.number, number=int(buffer))
        else:
            return None

    def _check_text(self) -> Optional[Token]:
        buffer: str = ''

        if self._source.get_char() == '"':
            self._source.pop_char()

            while self._source.get_char() != '"':
                buffer += self._source.pop_char()

            self._source.pop_char()
            return Token(LexType.text, text=buffer)
        else:
            return None

    def _check_inc_dec_operator(self) -> Optional[Token]:
        if self._source.get_char() == '+':
            self._source.pop_char()
            if self._source.get_char() == '+':
                self._source.pop_char()
                return Token(LexType.inc_op)
            else:
                return Token(LexType.add_op)
        elif self._source.get_char() == '-':
            self._source.pop_char()
            if self._source.get_char() == '-':
                self._source.pop_char()
                return Token(LexType.dec_op)
            else:
                return Token(LexType.sub_op)
        else:
            return None

    def _check_one_char_symbols(self) -> Token:
        char: str = self._source.pop_char()
        if char == '/':
            return Token(LexType.div_op)
        elif char == '*':
            return Token(LexType.mul_op)
        elif char == ':':
            return Token(LexType.card_op)
        elif char == '.':
            return Token(LexType.property_op)
        elif char == '{':
            return Token(LexType.left_curl_bracket)
        elif char == '}':
            return Token(LexType.right_curl_bracket)
        elif char == '(':
            return Token(LexType.left_bracket)
        elif char == ')':
            return Token(LexType.right_bracket)
        elif char == '=':
            return Token(LexType.assign_op)
        elif char == '$':
            return Token(LexType.eof)
        else:
            raise LexerError
