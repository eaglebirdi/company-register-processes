from typing import List, Tuple
from ..Configuration import Configuration
from .GeneralHelper import get_variable_name_for_sort

newline = Configuration.newline


def create_casefact_declaration_binary(predicate_name: str, sort1: str, sort2: str,
                                       instances: List[Tuple[str, str]]) -> str:
    var1 = get_variable_name_for_sort(sort1)
    var2 = get_variable_name_for_sort(sort2)
    if var1 == var2:
        var1 += "1"
        var2 += "2"

    disjunction = " | ".join([("(" + var1 + " = " + x + " & " + var2 + " = " + y + ")") for x, y in instances])

    if disjunction == "":
        disjunction = "$false"

    result = "tff(fact_" + predicate_name + ", axiom," + newline
    result += "  ! [" + var1 + ": " + sort1 + ", " + var2 + ": " + sort2 + "] :" + newline
    result += "  (" + newline
    result += "    " + predicate_name + "(" + var1 + ", " + var2 + ")" + newline
    result += "    <=>" + newline
    result += "    (" + newline
    result += "      " + disjunction + newline
    result += "    )" + newline
    result += "  )" + newline
    result += ")." + newline

    if Configuration.reassert_predicate_completion:
        cnt = 0
        for x, y in instances:
            cnt += 1
            result += "tff(fact_" + predicate_name + "_" + str(cnt) + ", axiom, "
            result += "$true => " + predicate_name + "(" + x + ", " + y + ")"
            result += ")." + newline

    return result


def create_casefact_declaration_monadic(predicate_name: str, sort: str, instances: List[str]) -> str:
    var1 = get_variable_name_for_sort(sort)
    disjunction = " | ".join([("(" + var1 + " = " + x + ")") for x in instances])

    if disjunction == "":
        disjunction = "$false"

    result = "tff(fact_" + predicate_name + ", axiom," + newline
    result += "  ! [" + var1 + ": " + sort + "] :" + newline
    result += "  (" + newline
    result += "    " + predicate_name + "(" + var1 + ")" + newline
    result += "    <=>" + newline
    result += "    (" + disjunction + ")" + newline
    result += "  )" + newline
    result += ")." + newline

    if Configuration.reassert_predicate_completion:
        cnt = 0
        for x in instances:
            cnt += 1
            result += "tff(fact_" + predicate_name + "_" + str(cnt) + ", axiom, "
            result += "$true => " + predicate_name + "(" + x + ")"
            result += ")." + newline

    return result


def create_casefact_declaration_ternary(predicate_name: str, sort1: str, sort2: str, sort3: str,
                                        instances: List[Tuple[str, str, str]]) -> str:
    var1 = get_variable_name_for_sort(sort1)
    var2 = get_variable_name_for_sort(sort2)
    var3 = get_variable_name_for_sort(sort3)
    if var1 == var2:
        if var1 == var3:
            var3 += "3"
        var1 += "1"
        var2 += "2"
    elif var1 == var3:
        var1 += "1"
        var3 += "3"
    if var2 == var3:
        var2 += "2"
        var3 += "3"

    disjunction = " | ".join([("(" + var1 + " = " + x + " & " + var2 + " = " + y + " & " + var3 + " = " + z + " )") for x, y, z in instances])

    if disjunction == "":
        disjunction = "$false"

    result = "tff(fact_" + predicate_name + ", axiom," + newline
    result += "  ! [" + var1 + ": " + sort1 + ", " + var2 + ": " + sort2 + ", " + var3 + ": " + sort3 + "] :" + newline
    result += "  (" + newline
    result += "    " + predicate_name + "(" + var1 + ", " + var2 + ", " + var3 + ")" + newline
    result += "    <=>" + newline
    result += "    (" + newline
    result += "      " + disjunction + newline
    result += "    )" + newline
    result += "  )" + newline
    result += ")." + newline

    if Configuration.reassert_predicate_completion:
        cnt = 0
        for x, y, z in instances:
            cnt += 1
            result += "tff(fact_" + predicate_name + "_" + str(cnt) + ", axiom, "
            result += "$true => " + predicate_name + "(" + x + ", " + y + ", " + z + ")"
            result += ")." + newline

    return result


def create_casefact_declaration_binary_grouped(predicate_name: str, sort1: str, sort2: str, instance1: str, instances2: List[str]) -> str:
    var1 = get_variable_name_for_sort(sort1)
    var2 = get_variable_name_for_sort(sort2)
    if var1 == var2:
        var1 += "1"
        var2 += "2"

    disjunction = " | ".join([("(" + var2 + " = " + x + ")") for x in instances2])

    if disjunction == "":
        disjunction = "$false"

    result = "tff(fact_" + predicate_name + "_" + instance1 + ", axiom," + newline
    result += "  ! [" + var1 + ": " + sort1 + ", " + var2 + ": " + sort2 + "] :" + newline
    result += "  (" + newline
    result += "    " + var1 + " = " + instance1 + newline
    result += "    =>" + newline
    result += "    (" + newline
    result += "      " + predicate_name + "(" + var1 + ", " + var2 + ")" + newline
    result += "      <=>" + newline
    result += "      (" + newline
    result += "        " + disjunction + newline
    result += "      )" + newline
    result += "    )" + newline
    result += "  )" + newline
    result += ")." + newline

    if Configuration.reassert_predicate_completion:
        cnt = 0
        for x in instances2:
            cnt += 1
            result += "tff(fact_" + predicate_name + "_" + instance1 + "_" + str(cnt) + ", axiom, "
            result += "$true => " + predicate_name + "(" + instance1 + ", " + x + ")"
            result += ")." + newline

    return result
