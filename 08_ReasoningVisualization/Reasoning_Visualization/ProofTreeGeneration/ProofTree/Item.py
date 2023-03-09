from typing import List, Union


class Item:
    def __init__(self, label: str, proposition: str, necessary: bool,
                 children: Union[None, List['Item']] = None):
        self.label = label
        self.proposition = proposition
        self.necessary = necessary
        self.children = children

    def __str__(self):
        return self.label
