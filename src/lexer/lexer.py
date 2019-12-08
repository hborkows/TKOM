from typing import Optional
from typing import Tuple
from typing import Dict
from src.lexer.token import Token
from src.source.source import Source
from src.lexer.lex_type import LexType


class Lexer:

    def __init__(self, source: Source):
        self._source = source

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


    def _skip_whitespace(self):
        while self._source.get_char().isspace():
            self._source.pop_char()

    def _check_keyword(self) -> Optional[Token]:
        keywords: Dict[str,LexType] = {
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
            'repeat': LexType.repeat_kw
        }
        functions: Tuple[str, str, str, str] = ('Player', 'Card', 'Token', 'Counter')
        buffer: str = ''

        if self._source.get_char().isalpha():
            buffer += self._source.pop_char()

            while self._source.get_char().isalnum():
                buffer += self._source.pop_char()

            if buffer in keywords.keys(): # buffer contains a keyword
                return Token(lex_type=keywords['buffer'])
            elif buffer in functions: # buffer contains an id of function
                return Token(lex_type=LexType.func_name, text=buffer)
            else: # buffer contains an object id
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


