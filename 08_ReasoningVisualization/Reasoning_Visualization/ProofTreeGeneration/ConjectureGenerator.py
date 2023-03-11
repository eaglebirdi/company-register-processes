from typing import List, Union
from .ContextInfo import ContextInfo
from .RuleAxiom.RuleAxiom import RuleAxiom
from .RuleAxiom.TypedVariable import TypedVariable
from .RuleAxiom.RuleOperand import RuleOperand
from .RuleAxiom.RelationOperand import RelationOperand
from .RuleAxiom.RelationStep import RelationStep


class ConjectureGenerator:
    def __init__(self, context: ContextInfo):
        self.context = context

    def generate(self, rule_operand: RuleOperand) -> str:
        path = self._create_path(rule_operand)
        proposition = self._create_proposition_from_path(rule_operand, path)
        return proposition

    def _create_path(self, start_operand: RuleOperand) -> List[RelationStep]:
        rule_operand = start_operand
        steps: List[RelationStep] = []

        cnt_layers = len(self.context.layers)
        for i in range(1, cnt_layers + 1):
            layer = self.context.layers[-i]

            if rule_operand not in layer.rule_operands:
                raise Exception("Rule operand must occur in the current rule axiom.")

            subpath = self._navigate_to_universal_variable(rule_operand.argument, layer, [], 0)
            if subpath is None:
                raise Exception("Path to universal variable could not be found.")

            steps += subpath

            if i < cnt_layers:
                next_layer = self.context.layers[-i - 1]
                rule_operand = next_layer.get_rule_operand(layer.predicate_name)
                if rule_operand is None:
                    raise Exception("Layer switch could not be conducted.")

        return steps

    def _navigate_to_universal_variable(self, variable: TypedVariable, rule_axiom: RuleAxiom,
                                        visited_relations: List[RelationOperand], lvl: int)\
            -> Union[List[RelationStep], None]:
        if lvl > 100:
            raise Exception("Aborted due to possible endless recursion.")

        if variable == rule_axiom.universal_variable:
            return []

        adjacent_relations = self._get_adjacent_relations(variable, rule_axiom)

        for relation_step in adjacent_relations:
            relation = relation_step.operand
            if relation_step.operand in visited_relations:
                continue
            next_variable = relation.argument1 if relation_step.reverse else relation.argument2
            path = self._navigate_to_universal_variable(next_variable, rule_axiom, visited_relations + [relation], lvl+1)
            if path is not None:
                return [relation_step] + path

        return None

    def _get_adjacent_relations(self, variable: TypedVariable, rule_axiom: RuleAxiom) -> List[RelationStep]:
        ret_list: List[RelationStep] = []

        for relation_operand in rule_axiom.relation_operands:
            if relation_operand.argument1.variable_name == variable.variable_name:
                ret_list.append(RelationStep(relation_operand, False))
            elif relation_operand.argument2.variable_name == variable.variable_name:
                ret_list.append(RelationStep(relation_operand, True))

        return ret_list

    def _create_proposition_from_path(self, rule_operand: RuleOperand, path: List[RelationStep]) -> str:
        first_variable = "X0"
        var_name_prev = first_variable
        variables: List[str] = [var_name_prev + ": " + rule_operand.argument.variable_type]
        predicates: List[str] = []

        cnt = 0
        for relation_step in path:
            cnt += 1
            var_name = "X" + str(cnt)
            if relation_step.reverse:
                variables.append(var_name + ": " + relation_step.operand.argument1.variable_type)
                predicates.append(relation_step.operand.predicate_name + "(" + var_name + ", " + var_name_prev + ")")
            else:
                variables.append(var_name + ": " + relation_step.operand.argument2.variable_type)
                predicates.append(relation_step.operand.predicate_name + "(" + var_name_prev + ", " + var_name + ")")
            var_name_prev = var_name

        predicates.append(rule_operand.predicate_name + "(" + first_variable + ")")
        result = "? [" + ", ".join(variables) + "]: (" + " & ".join(predicates) + ")"
        return result
