from typing import List, Union, Tuple, Dict
from .RuleAxiom.RuleAxiom import RuleAxiom
from .RuleAxiom.TypedVariable import TypedVariable
from .RuleAxiom.RuleOperand import RuleOperand
from .RuleAxiom.RelationOperand import RelationOperand
from AxiomTextParsing import *


class RuleAxiomExaminer:
    def __init__(self):
        pass

    def examine(self, axioms: List[TFFAnnotated]) -> Dict[str, RuleAxiom]:
        result = dict()
        for axiom in axioms:
            rule_axiom, _ = self._examine_single_axiom(axiom)
            if rule_axiom is not None:
                rule_name = rule_axiom.predicate_name
                if rule_name in result:
                    raise Exception("The rule axiom '" + rule_name + "' exists more than once.")
                else:
                    result[rule_name] = rule_axiom
        return result

    def _examine_single_axiom(self, axiom: TFFAnnotated) -> Tuple[Union[RuleAxiom, None], str]:
        result_split_head_and_body, msg = self._split_head_and_body(axiom)
        if result_split_head_and_body is None:
            return None, msg
        atomic_head, rule_body, (quantified_variable_name, quantified_variable_type) = result_split_head_and_body

        result_extract_existvars, msg = self._extract_existential_variables(rule_body)
        if result_extract_existvars is None:
            return None, msg
        existential_variables, inner_body = result_extract_existvars
        universal_variable = TypedVariable(quantified_variable_name, quantified_variable_type.name)

        all_variables = [universal_variable] + existential_variables

        result_extract_operands, msg = self._extract_operands(inner_body, all_variables)
        if result_extract_operands is None:
            return None, msg
        rule_operands, relation_operands, is_disjunction = result_extract_operands

        return RuleAxiom(atomic_head.f, is_disjunction,
                         universal_variable, existential_variables,
                         rule_operands, relation_operands), ""

    def _split_head_and_body(self, axiom: TFFAnnotated) -> Tuple[Union[None, Tuple[AtomicFormula, Formula, Tuple[str, AtomicType]]], str]:
        if axiom.formula is None:
            return None, "Axiom has no formula"

        if not isinstance(axiom.formula, Logical):
            return None, "Formula must be Logical"

        if not isinstance(axiom.formula.formula, QuantifiedFormula):
            return None, "Formula must be QuantifiedFormula"
        quantified_formula: QuantifiedFormula = axiom.formula.formula

        if quantified_formula.quantifier != '!':
            return None, "Quantifier must be universal"

        variable_list = quantified_formula.variableList
        if len(variable_list) != 1:
            return None, "It must be quantified over exactly one variable"
        quantified_variable: Tuple[str, Type] = variable_list[0]
        quantified_variable_name = quantified_variable[0]
        quantified_variable_type = quantified_variable[1]

        if not isinstance(quantified_variable_type, AtomicType):
            return None, "Universally quantified variable must be of an atomic type but was " + str(type(quantified_variable_type))

        # ToDo check quantified_variable_type.args

        body = quantified_formula.body
        if not isinstance(body, BinaryFormula):
            return None, "The quantification body must be a binary formula"
        binary_formula: BinaryFormula = body

        if binary_formula.connective == '=>':
            rule_head = binary_formula.right
            rule_body = binary_formula.left
        elif binary_formula.connective == '<=':
            rule_head = binary_formula.left
            rule_body = binary_formula.right
        elif binary_formula.connective == '<=>':
            # ToDo this could be more elaborate
            rule_head = binary_formula.left
            rule_body = binary_formula.right
        else:
            return None, "The connector " + binary_formula.connective + " is not supported in the rule body's root"

        if not isinstance(rule_head, AtomicFormula):
            return None, "Rule head must be an atomic formula"
        atomic_head: AtomicFormula = rule_head


        if len(atomic_head.args) != 1:
            return None, "Rule head predicate must have exactly one argument"

        head_arg = atomic_head.args[0]
        if not isinstance(head_arg, Variable):
            return None, "Argument of rule head predicate must be a variable"
        head_var: Variable = head_arg

        if head_var.name != quantified_variable_name:
            return None, "Variable argument of rule head must be '" + quantified_variable_name


        return (atomic_head, rule_body, (quantified_variable_name, quantified_variable_type)), ""

    def _extract_existential_variables(self, rule_body: Formula) -> Tuple[Union[Tuple[List[TypedVariable], Formula], None], str]:
        if isinstance(rule_body, QuantifiedFormula):
            if rule_body.quantifier != '?':
                return None, "Not supported rule for non-existentially quantified formula"

            existential_variables = []

            for var in rule_body.variableList:
                existential_variable_name = var[0]
                existential_variable_type = var[1]
                if not isinstance(existential_variable_type, AtomicType):
                    return None, "Existential variable '" + var[0] + "' type must be AtomicType: "
                existential_variables.append(TypedVariable(existential_variable_name, existential_variable_type.name))

            inner_body = rule_body.body
        else:
            existential_variables = []
            inner_body = rule_body

        return (existential_variables, inner_body), ""

    def _extract_operands(self, inner_body: Formula, all_variables: List[TypedVariable])\
            -> Tuple[Union[Tuple[List[RuleOperand], List[RelationOperand], bool], None], str]:
        flattened_operands, operator = self._flatten_operands(inner_body, None, 0)
        is_disjunction = operator == '|'
        rule_operands, relation_operands, other_operands = self._parse_operand_types(flattened_operands, all_variables)

        if len(other_operands) > 0:
            return None, "Only valid rule and relation predicates allowed"

        if len(rule_operands) == 0:
            return None, "There must be at least one subordinate rule operand"

        if len(all_variables) > 1 and is_disjunction:
            return None, "Existential formula must not be a disjunction"

        if len(all_variables) == 1 and len(relation_operands) > 0:
            return None, "Plain conjunction/disjunction may only contain rule operands"

        return (rule_operands, relation_operands, is_disjunction), ""

    def _parse_operand_types(self, operands: List[Formula], all_variables: List[TypedVariable])\
        -> Tuple[List[RuleOperand], List[RelationOperand], List[Tuple[AtomicFormula, str]]]:
        rule_operands = []
        relation_operands = []
        other_operands = []

        for operand in operands:
            if isinstance(operand, AtomicFormula):
                if len(operand.args) == 1:
                    (arg0, ) = operand.args
                    if isinstance(arg0, Variable):
                        variable = self._find_variable(all_variables, arg0.name)
                        if variable is None:
                            other_operands.append((operands, "There is no quantified variable '" + arg0.name + "'"))
                        else:
                            rule_operands.append(RuleOperand(operand.f, variable))
                    else:
                        other_operands.append((operand, "Monadic predicate with non-variable argument"))
                elif len(operand.args) == 2:
                    (arg0, arg1) = operand.args
                    if isinstance(arg0, Variable) and isinstance(arg1, Variable):
                        variable1 = self._find_variable(all_variables, arg0.name)
                        variable2 = self._find_variable(all_variables, arg1.name)
                        if variable1 is None:
                            other_operands.append((operands, "There is no quantified variable '" + arg0.name + "'"))
                        elif variable2 is None:
                            other_operands.append((operands, "There is no quantified variable '" + arg1.name + "'"))
                        else:
                            relation_operands.append(RelationOperand(operand.f, variable1, variable2))
                    else:
                        other_operands.append((operand, "Binary predicate with non-variable arguments"))
                else:
                    other_operands.append((operand, "Both non-monadic and non-binary predicate"))
            else:
                other_operands.append((operand, "Non-atomic formula"))

        return rule_operands, relation_operands, other_operands

    def _find_variable(self, all_variables: List[TypedVariable], name: str) -> Union[TypedVariable, None]:
        res = [x for x in all_variables if x.variable_name == name]
        if len(res) == 1:
            return res[0]
        else:
            return None

    """
    Flattens the binary formula to a list of equipollent operands.
    """
    def _flatten_operands(self, formula: Formula, operator: Union[str, None], lvl: int) -> Tuple[List[Formula], str]:
        if lvl > 100:
            raise Exception("Aborted due to possible endless recursion.")

        if not isinstance(formula, BinaryFormula):
            return [formula], '&'

        if operator is not None and operator != formula.connective:
            return [formula], operator

        left, _ = self._flatten_operands(formula.left, formula.connective, lvl+1)
        right, _ = self._flatten_operands(formula.right, formula.connective, lvl+1)

        return left + right, formula.connective
