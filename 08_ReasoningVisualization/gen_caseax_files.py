import json
import os
from CaseAxiomGeneration import A96_DirectorAppointment_Generator
from CaseAxiomGeneration import A115_CompanyDissolution_Generator
from CaseAxiomGeneration import A108_CapitalIncrease_Generator
from CaseAxiomGeneration import Configuration


def execute(key, root_rule, precompute_arithmetics, reassert_predcompl):
    config = Configuration(precompute_arithmetics, reassert_predcompl)
    folder = os.path.join("./ExampleCases", key)

    if "A96" in key:
        generator = A96_DirectorAppointment_Generator(config)
    elif "A115" in key:
        generator = A115_CompanyDissolution_Generator(config)
    elif "A108" in key:
        generator = A108_CapitalIncrease_Generator(config)
    else:
        raise Exception("not supported")

    with open(os.path.join(folder, "example.json"), 'r') as fi:
        case_data_json = json.load(fi)

    gen_result = generator.create(case_data_json, root_rule)
    case_related_axioms = gen_result.axiom_files

    instances_ax_file = [x for x in case_related_axioms if x.name == 'instances.ax'][0]
    with open(os.path.join(folder, "instances.ax"), 'w') as fi:
        fi.write(instances_ax_file.content)

    casefacts_ax_file = [x for x in case_related_axioms if x.name == 'casefacts.ax'][0]
    with open(os.path.join(folder, "casefacts.ax"), 'w') as fi:
        fi.write(casefacts_ax_file.content)


def main():
    root_rule = "is_application_legal"
    precompute_arithmetics = False
    reassert_predcompl = False

    key = "A96_DirectorAppointment"
    # key = "A115_CompanyDissolution"
    # key = "A108_CapitalIncrease"

    execute(key, root_rule, precompute_arithmetics, reassert_predcompl)
    print("Generation finished for " + key)


if __name__ == '__main__':
    main()
