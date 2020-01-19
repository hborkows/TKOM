import unittest
from tests.test_lexer.test_lexer import TestLexer
from tests.test_lexer.test_source import TestSource
from tests.test_parser.test_parser import TestParser
from tests.test_interpreter.test_interpreter import TestInterpreter

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromTestCase(TestSource))
suite.addTests(loader.loadTestsFromTestCase(TestLexer))
suite.addTests(loader.loadTestsFromTestCase(TestParser))
suite.addTests(loader.loadTestsFromTestCase(TestInterpreter))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
