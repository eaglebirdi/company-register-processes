from typing import List, Union
from .ProofStatus import ProofStatus


class Item:
    def __init__(self, label: str, proposition: str, necessary: bool,
                 children: Union[None, List['Item']] = None,
                 proof_status: Union[None, ProofStatus] = None):
        self.label = label
        self.proposition = proposition
        self.necessary = necessary
        self.children = children
        self.proof_status = proof_status
