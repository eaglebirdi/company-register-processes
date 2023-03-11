from typing import List, Callable
from .DataStructures import *


def assert_length(args: List, count: int):
    actual = len(args)
    if actual != count:
        raise Exception("assert_length failed: Should be " + str(count) + " but was " + str(actual))


class Dict2StructuresConverter:
    def __init__(self):
        pass

    def convert(self, dictionary: dict):
        result = self._parse_inner(dictionary)
        return result

    def _parse_inner(self, dictionary: dict, special_logic: Callable = None):
        name = dictionary['_name']
        args = dictionary.get('args')

        if name == 'Vector' or name == 'List':
            return [self._parse_inner(x, special_logic) for x in args]
        elif name == 'None':
            return None
        elif name == '':
            if special_logic is None:
                raise Exception("empty name and no special logic")
            return special_logic(dictionary)
        elif name == 'Some':
            assert_length(args, 1)
            return self._parse_inner(args[0])
        elif name == 'TFFAnnotated':
            assert_length(args, 4)
            return TFFAnnotated(
                self._extract_string(args[0]),
                self._extract_string(args[1]),
                self._parse_inner(args[2])
            )
        elif name == 'AtomicType':
            assert_length(args, 2)
            return AtomicType(
                self._extract_string(args[0]),
                self._parse_inner(args[1])
            )
        elif name == 'AtomicTerm':
            assert_length(args, 2)
            return AtomicTerm(
                self._extract_string(args[0]),
                self._parse_inner(args[1])
            )
        elif name == 'Variable':
            assert_length(args, 1)
            return Variable(
                self._extract_string(args[0])
            )
        elif name == 'Logical':
            assert_length(args, 1)
            return Logical(
                self._parse_inner(args[0])
            )
        elif name == 'AtomicFormula':
            assert_length(args, 2)
            return AtomicFormula(
                self._extract_string(args[0]),
                self._parse_inner(args[1])
            )
        elif name == 'QuantifiedFormula':
            assert_length(args, 3)
            return QuantifiedFormula(
                self._extract_string(args[0]),
                self._parse_inner(args[1], self._variable_list_logic),
                self._parse_inner(args[2])
            )
        elif name == 'UnaryFormula':
            assert_length(args, 2)
            return UnaryFormula(
                self._extract_string(args[0]),
                self._parse_inner(args[1])
            )
        elif name == 'BinaryFormula':
            assert_length(args, 3)
            return BinaryFormula(
                self._extract_string(args[0]),
                self._parse_inner(args[1]),
                self._parse_inner(args[2])
            )
        elif name == 'Equality':
            assert_length(args, 2)
            return Equality(
                self._parse_inner(args[0]),
                self._parse_inner(args[1])
            )
        elif name == 'Inequality':
            assert_length(args, 2)
            return Inequality(
                self._parse_inner(args[0]),
                self._parse_inner(args[1])
            )
        elif name == 'FormulaVariable':
            assert_length(args, 1)
            return FormulaVariable(
                self._extract_string(args[0])
            )
        elif name == 'NumberTerm':
            assert_length(args, 1)
            return NumberTerm(
                self._parse_inner(args[0])
            )
        elif name == 'Integer':
            assert_length(args, 1)
            return Integer(int(args[0]['_name']))
        elif name == 'Rational':
            assert_length(args, 2)
            return Rational(int(args[0]['_name']), int(args[1]['_name']))
        elif name == 'Real':
            assert_length(args, 3)
            return Real(int(args[0]['_name']), int(args[1]['_name']), int(args[2]['_name']))
        elif name == 'Typing':
            assert_length(args, 2)
            return Typing(
                self._extract_string(args[0]),
                self._parse_inner(args[1])
            )
        elif name == 'MappingType':
            assert_length(args, 2)
            return MappingType(
                self._parse_inner(args[0]),
                self._parse_inner(args[1])
            )
        else:
            raise Exception("not yet implemented: " + name)

    def _variable_list_logic(self, obj: dict):
        name = obj['_name']
        args = obj['args']

        if name != '':
            raise Exception("name must be empty")

        return (
            self._extract_string(args[0]),
            self._parse_inner(args[1])
        )

    def _extract_string(self, obj: dict) -> str:
        name = obj['_name']
        args = obj.get('args')

        if args is not None:
            raise Exception("args must not exist for " + name)

        return name
