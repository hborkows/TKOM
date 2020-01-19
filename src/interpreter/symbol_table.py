from src.interpreter.symbol import Symbol
from typing import Optional, Dict, List


class SymbolTable:

    def __init__(self):
        self._symbol_table: Dict[str: Symbol] = {}

    def add_symbol(self, symbol: Symbol):
        self._symbol_table[symbol.name] = symbol

    def is_symbol_defined(self, name: str) -> bool:
        return name in self._symbol_table.keys()

    def get_symbol_by_name(self, name: str) -> Optional[Symbol]:
        if self.is_symbol_defined(name):
            return self._symbol_table[name]
        else:
            return None

    def get_symbols_by_type(self, symbol_type: str) -> List[Symbol]:
        result: List[Symbol] = []
        for symbol in self._symbol_table.values():
            if symbol.symbol_type == symbol_type or symbol_type == 'any':
                result.append(symbol)
        return result

    def remove_symbol_by_name(self, name: str):
        self._symbol_table.pop(name)

    def remove_symbols_by_type(self, symbol_type: str):
        for item in self.get_symbols_by_type(symbol_type=symbol_type):
            self.remove_symbol_by_name(item.name)

    def clear(self):
        self._symbol_table = {}
