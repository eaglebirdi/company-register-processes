from typing import List


class Item:
    def __init__(self, label: str, proposition: str, necessary: bool, children: List['Item']):
        self.label = label
        self.proposition = proposition
        self.necessary = necessary
        self.children = children
    