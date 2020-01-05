from typing import List, Optional


class ASTNode(object):

    def get_representation(self) -> str:
        pass

    def get_children(self) -> Optional[List]:
        pass
