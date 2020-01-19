import unittest
from src.interpreter.interpreter import Interpreter
from src.parser.parser import Parser
from src.lexer.lexer import Lexer
from src.source.source import Source


class TestInterpreter(unittest.TestCase):

    def setUp(self) -> None:
        self.interpreter = Interpreter(parser=Parser(lexer=Lexer(source=Source())))

    def test(self):
        pass
