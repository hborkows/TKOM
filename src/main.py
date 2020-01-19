from src.interpreter.interpreter import Interpreter, InterpreterError
from src.parser.parser import Parser, ParserError
from src.lexer.lexer import Lexer, LexerError
from src.source.source import Source


def main():
    source = Source()
    lexer = Lexer(source)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)

    while True:
        text = input('==>')
        source.set_code_line(line=text)
        #print(source.get_char())
        #try:
        interpreter.interpret()
        '''except LexerError:
            print('Lexer error.')
        except ParserError:
            print('Parsing error.')
        except InterpreterError:
            print('Error during runtime.')'''


if __name__ == "__main__":
    main()
