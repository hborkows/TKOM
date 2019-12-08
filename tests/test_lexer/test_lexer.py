import unittest
from typing import Dict, Tuple

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
        self.assertEqual(token.text, 'Hubert')

        self.lexer.get_source().set_code_line('lowercase_id')
        token = self.lexer.next_token()
        self.assertEqual(token.type, LexType.object_id)
        self.assertEqual(token.text, 'lowercase_id')

    def test_function_name(self):
        functions: Tuple[str, str, str, str] = ('Player', 'Card', 'Token', 'Counter')

        for function in functions:
            self.lexer.get_source().set_code_line(function)
            token = self.lexer.next_token()
            self.assertEqual(token.type, LexType.func_name)
            self.assertEqual(token.text, function)

    def test_keyword(self):
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

        for keyword in keywords.keys():
            self.lexer.get_source().set_code_line(keyword)
            token = self.lexer.next_token()
            self.assertEqual(token.type, keywords[keyword])

    def test_number(self):
        self.lexer.get_source().set_code_line('17')
        token = self.lexer.next_token()
        self.assertEqual(token.type, LexType.number)
        self.assertEqual(token.number, 17)

    def test_text(self):
        self.lexer.get_source().set_code_line('"Jace, the Mind Sculptor"')
        token = self.lexer.next_token()
        self.assertEqual(token.type, LexType.text)
        self.assertEqual(token.text, 'Jace, the Mind Sculptor')

    def test_symbols(self):
        symbols: Dict[str, LexType] = {
            '++': LexType.inc_op, '--': LexType.dec_op, '+': LexType.add_op, '-': LexType.sub_op,
            '/': LexType.div_op, '*': LexType.mul_op, ':': LexType.card_op, '.': LexType.property_op,
            '{': LexType.left_curl_bracket, '}': LexType.right_curl_bracket, '(': LexType.left_bracket,
            ')': LexType.right_bracket, '=': LexType.assign_op
        }

        for symbol in symbols.keys():
            self.lexer.get_source().set_code_line(symbol)
            token = self.lexer.next_token()
            self.assertEqual(token.type, symbols[symbol])

    def test_raise_error_when_unknown_input(self):
        self.lexer.get_source().set_code_line('%^^&%&&*ERROR##@!@')
        self.assertRaises(LexerError, self.lexer.next_token)
