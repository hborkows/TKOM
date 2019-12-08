import unittest
from src.lexer.lex_type import LexType
from src.lexer.lexer import Lexer
from src.lexer.lexer import LexerError
from src.source.source import Source


class TestLexer(unittest.TestCase):

    def setUp(self) -> None:
        self.lexer = Lexer(source=Source())

    def test__object_id(self):
        self.lexer.get_source().set_code_line('Hubert')
        token = self.lexer.next_token()
        self.assertEqual(token.type, LexType.object_id)

    def test_function_name(self):
        pass

    def test_keyword(self):
        pass

    def test_number(self):
        pass

    def test_text(self):
        pass

    def test_operators(self):
        pass

    def test_raise_error_when_unknown_input(self):
        pass
