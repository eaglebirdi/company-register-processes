from abc import ABC
from typing import List, Tuple

'''
types are partially taken from
https://github.com/leoprover/scala-tptp-parser/blob/master/src/main/scala/leo/datastructures/TPTP.scala
'''


class Type(ABC):
    def __init__(self):
        pass


class AtomicType(Type):
    def __init__(self, name: str, args: List[Type]):
        super().__init__()
        self.name = name
        self.args = args


class AnnotatedFormula(ABC):
    def __init__(self):
        pass


class Statement(ABC):
    def __init__(self):
        pass


class Term(ABC):
    def __init__(self):
        pass


class AtomicTerm(Term):
    def __init__(self, f: str, args: List[Term]):
        super().__init__()
        self.f = f
        self.args = args


class Variable(Term):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


class Connective(ABC):
    def __init__(self):
        pass


class UnaryConnective(Connective, ABC):
    def __init__(self):
        super().__init__()


class BinaryConnective(Connective, ABC):
    def __init__(self):
        super().__init__()


class TFFAnnotated(AnnotatedFormula):
    def __init__(self, name: str, role: str, formula: Statement):
        super().__init__()
        self.name = name
        self.role = role
        self.formula = formula
        # self.annotations = annotations


class Formula(ABC):
    def __init__(self):
        pass


class Logical(Statement):
    def __init__(self, formula: Formula):
        super().__init__()
        self.formula = formula


class AtomicFormula(Formula):
    def __init__(self, f: str, args: List[Term]):
        super().__init__()
        self.f = f
        self.args = args


class QuantifiedFormula(Formula):
    def __init__(self, quantifier: str, variablelist: List[Tuple[str, Type]], body: Formula):
        super().__init__()
        self.quantifier = quantifier
        self.variableList = variablelist
        self.body = body


class UnaryFormula(Formula):
    def __init__(self, connective: str, body: Formula):
        super().__init__()
        self.connective = connective
        self.body = body


class BinaryFormula(Formula):
    def __init__(self, connective: str, left: Formula, right: Formula):
        super().__init__()
        self.connective = connective
        self.left = left
        self.right = right


class Equality(Formula):
    def __init__(self, left: Term, right: Term):
        super().__init__()
        self.left = left
        self.right = right


class Inequality(Formula):
    def __init__(self, left: Term, right: Term):
        super().__init__()
        self.left = left
        self.right = right


class FormulaVariable(Formula):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


class Number(ABC):
    pretty = None

    def __init__(self):
        super().__init__()


class Integer(Number):
    def __init__(self, value: int):
        super().__init__()
        self.pretty = str(value)


class Rational(Number):
    def __init__(self, numerator: int, denominator: int):
        super().__init__()
        self.pretty = str(numerator) + "/" + str(denominator)


class Real(Number):
    def __init__(self, wholepart: int, decimalplaces: int, exponent: int):
        super().__init__()
        if exponent == 1:
            self.pretty = str(wholepart) + "." + str(decimalplaces)
        else:
            self.pretty = str(wholepart) + "." + str(decimalplaces) + "E" + str(exponent)


class NumberTerm(Formula):
    def __init__(self, value: Number):
        super().__init__()
        self.pretty = value.pretty


class Typing(Statement):
    def __init__(self, atom: str, typ: Type):
        super().__init__()
        self.atom = atom
        self.typ = typ


class MappingType(Type):
    def __init__(self, left: List[Type], right: Type):
        super().__init__()
        self.left = left
        self.right = right
