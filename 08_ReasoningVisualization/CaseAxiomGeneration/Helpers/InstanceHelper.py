from typing import List
from itertools import combinations
from ..Configuration import Configuration
from .GeneralHelper import get_variable_name_for_sort

newline = Configuration.newline


class InstanceHelper:
    def __init__(self, reassert_predicate_completion: bool):
        self.reassert_predicate_completion = reassert_predicate_completion

    def create_instance_declaration(self, name: str, sort: str) -> str:
        result = "tff(inst_" + name + ", type, " + name + " : " + sort + ")." + newline
        return result

    def create_inequality_constraints(self, names: List[str]) -> str:
        result = ""

        pairs = list(combinations(names, 2))
        for p1, p2 in pairs:
            result += "tff(inequality_" + p1 + "_" + p2 + ", axiom, " + p1 + " != " + p2 + ")." + newline

        return result

    def create_relation_declaration(self, predicate_name: str, sort1: str, sort2: str, individual1: str, individual2: str):
        var1 = get_variable_name_for_sort(sort1)
        var2 = get_variable_name_for_sort(sort2)
        result = "tff(relation_" + predicate_name + ", axiom," + newline
        result += "  ! [" + var1 + ": " + sort1 + ", " + var2 + ": " + sort2 + "] :" + newline
        result += "  (" + newline
        result += "    " + predicate_name + "(" + var1 + ", " + var2 + ")" + newline
        result += "    <=>" + newline
        result += "    (" + newline
        result += "      " + var1 + " = " + individual1 + " & " + var2 + " = " + individual2 + newline
        result += "    )" + newline
        result += "  )" + newline
        result += ")." + newline

        if self.reassert_predicate_completion:
            result += "tff(relation_" + predicate_name + "_1, axiom, "
            result += "$true => " + predicate_name + "(" + individual1 + ", " + individual2 + ")"
            result += ")." + newline

        return result
