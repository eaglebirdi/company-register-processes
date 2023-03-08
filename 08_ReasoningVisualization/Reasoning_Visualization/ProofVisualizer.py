from typing import Tuple
from colorama import Fore, Back, Style
from .ProofTreeGeneration.Tree import Tree
from .ProofTreeGeneration.Item import Item
from .ProofTreeGeneration.EnrichedItem import EnrichedItem
from .ProofTreeGeneration.ProofStatus import ProofStatus

color_proved = Fore.GREEN
color_nonproved_necessary = Back.RED + Fore.BLACK
color_nonproved_nonnecessary = Fore.WHITE
color_timeout = Fore.CYAN
color_error = Fore.YELLOW
color_default = ''

icon_proved = "\u2713"
icon_nonproved = "\u2717"
icon_timeout = "\u231A"
icon_error = "\u26A0"
icon_default = "\u2610"

style_reset = Style.RESET_ALL

indent = "  "


class ProofVisualizer:
    def __init__(self, proof_tree: Tree):
        self.proof_tree = proof_tree

    def print(self) -> None:
        self._print(self.proof_tree.root, 0)

    def _print(self, item: Item, lvl: int) -> None:
        if lvl > 100:
            raise Exception("Aborted due to possible endless recursion.")

        color, icon = self._get_color_and_icon(item)

        text = lvl*indent + color + icon + " " + item.label + "?" + style_reset
        print(text)

        if item.children is not None:
            for child in item.children:
                self._print(child, lvl+1)

    def _get_color_and_icon(self, item: Item) -> Tuple[str, str]:
        if not isinstance(item, EnrichedItem):
            return color_default, icon_default

        if item.proof_status == ProofStatus.PROVED:
            return color_proved, icon_proved
        elif item.proof_status == ProofStatus.NOT_PROVED:
            if item.necessary:
                return color_nonproved_necessary, icon_nonproved
            else:
                return color_nonproved_nonnecessary, icon_nonproved
        elif item.proof_status == ProofStatus.TIMEOUT:
            return color_timeout, icon_timeout
        elif item.proof_status == ProofStatus.ERROR:
            return color_error, icon_error
        else:
            return color_default, icon_default
