from typing import List, Union
from .Item import Item
from .ProofStatus import ProofStatus
from ..TPTPProgram import TPTPProgram


class EnrichedItem(Item):
    def __init__(self, label: str, proposition: str, necessary: bool,
                 tptp_program: TPTPProgram,
                 children: Union[None, List['EnrichedItem']] = None):
        super().__init__(label, proposition, necessary, children)
        self.tptp_program = tptp_program
        self.proof_status: Union[ProofStatus, None] = None
