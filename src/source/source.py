

class Source:

    def __init__(self):
        self._code_line: str = ''

    def set_code_line(self, line: str):
        self._code_line = line
        
    def get_char(self) -> str:
        if self._code_line:
            return self._code_line[0]
        else:
            return '$'
    
    def pop_char(self) -> str:
        if len(self._code_line) > 1:
            result: str = self._code_line[0]
            self._code_line = self._code_line[1:]
        elif self._code_line:
            result: str = self._code_line[0]
            self._code_line = ''
        else:
            result: str = '$'

        return result
