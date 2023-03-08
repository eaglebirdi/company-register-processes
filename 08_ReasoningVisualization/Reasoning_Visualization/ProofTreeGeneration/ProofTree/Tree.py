from .Item import Item


class Tree:
    def __init__(self, main_object: str, root: Item):
        self.main_object = main_object
        self.root = root
