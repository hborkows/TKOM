from typing import Optional, List
from src.ast.instruction import Instruction
from src.ast.object import Object
from src.ast.definition import Definition


class Assignment(Instruction):

    def __init__(self, object: Object, definition: Definition):
        self.object = object
        self.definition = definition

    def get_representation(self) -> str:
        return 'Assignment'

    def get_children(self) -> Optional[List]:
        return [self.object, self.definition]
