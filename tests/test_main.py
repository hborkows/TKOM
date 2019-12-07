import unittest
from tests.test_add import TestAdd

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromTestCase(TestAdd))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
