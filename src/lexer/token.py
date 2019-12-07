from src.lexer.lex_type import LexType


class Token:

    def __init__(self, lex_type: LexType, text='', number=0):
        self.type = lex_type
        self.text = text
        self.number = number
