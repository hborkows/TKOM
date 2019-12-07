import unittest
from src.source.source import Source


class TestSource(unittest.TestCase):

    def test_return_when_line_empty(self):
        source = Source()
        self.assertEqual(source.get_char(), '$')
        self.assertEqual(source.pop_char(), '$')

    def test_pop_when_line_not_empty(self):
        source = Source()
        test_line = 'Test line'
        source.set_code_line(test_line)

        for char in test_line:
            self.assertEqual(source.pop_char(), char)

    def test_get_when_line_not_empty(self):
        source = Source()
        test_char = 'E'
        source.set_code_line(test_char)

        self.assertEqual(source.get_char(), test_char)
