from typing import List


def get_variable_name_for_sort(sort: str) -> str:
    if sort.startswith("$"):
        return "X"
    else:
        return sort.capitalize()


def create_disjunction(operators: List[str]) -> str:
    result = ""
    for i in range(len(operators)):
        if i > 0:
            result += " | "
        result += operators[i]
    return result


def is_empty(value: str) -> bool:
    if value is None:
        return True
    if value == "":
        return True
    return False
