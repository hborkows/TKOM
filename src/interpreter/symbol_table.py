from src.interpreter.symbol import Symbol
from typing import List, Optional, Dict


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
