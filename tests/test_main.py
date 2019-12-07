import unittest
from tests.test_lexer.test_lexer import TestLexer

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromTestCase(TestLexer))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
