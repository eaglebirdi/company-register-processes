import argparse
import json
from CaseAxiomGeneration import Configuration, A96_DirectorAppointment_Generator, A115_CompanyDissolution_Generator, A108_CapitalIncrease_Generator
from ApplicationProcessImplementation import ApplicationProcessImplementation
from reasvis import execute


application_processes = [
    ApplicationProcessImplementation(
        "A96", "DirectorAppointment",
        lambda config: A96_DirectorAppointment_Generator(config)),
    ApplicationProcessImplementation(
        "A115", "CompanyDissolution",
        lambda config: A115_CompanyDissolution_Generator(config)),
    ApplicationProcessImplementation(
        "A108", "CapitalIncrease",
        lambda config: A108_CapitalIncrease_Generator(config))
    ]


def find_application_process(search_text: str) -> ApplicationProcessImplementation:
    hits = [x for x in application_processes if
            x.gustavus_key == search_text or
            x.name == search_text or
            x.combined_key == search_text]
    if len(hits) > 0:
        return hits[0]
    else:
        allowed_keys = ", ".join([x.gustavus_key for x in application_processes])
        raise Exception("The application process " + search_text + " does not exist. Possible values: " + allowed_keys)


def main():
    parser = argparse.ArgumentParser("Visualize reasoning for company register application process")
    parser.add_argument("--process", required=True, help="Name of the application process")
    parser.add_argument("--prover", required=True, help="Name of the ATP tool. Allowed values: cvc5, iprover, leo3, princess, vampire")
    parser.add_argument("--timeout", default=3, help="Timeout in seconds for each prover invocation")
    parser.add_argument("--precompute_arithmetics", action='store_true', help="Whether arithmetic reasoning in precomputed")
    parser.add_argument("--reassert_predicate_completion", action='store_true', help="Whether the case-related axioms are individually asserted again in addition to the predicate completion")
    parser.add_argument("--single_file_axioms", action='store_true', help="Whether the axioms are merged into one single file")
    parser.add_argument("case_data_file", help="Name of the case data JSON file")

    args = parser.parse_args()

    application_process = find_application_process(args.process)

    if args.precompute_arithmetics:
        application_process_path = application_process.get_package_path_without_arithmetic()
    else:
        application_process_path = application_process.get_package_path()

    with open(application_process_path, 'rb') as fi:
        application_process_data = fi.read()

    with open(args.case_data_file, 'r') as fi:
        case_data_json = json.load(fi)

    root_rule = application_process.root_rule

    case_axiom_config = Configuration(args.precompute_arithmetics, args.reassert_predicate_completion)
    case_axiom_generator = application_process.case_axiom_generator_retrieval(case_axiom_config)
    generation_result = case_axiom_generator.create(case_data_json, root_rule)

    case_axioms = generation_result.axiom_files
    main_object = generation_result.main_object

    execute(application_process_data, case_axioms,
            args.prover, args.timeout,
            root_rule, main_object,
            args.single_file_axioms)


'''
Exemplary command line arguments:
--process A96 --prover cvc5 --reassert_predicate_completion ./case_data.json
--process A96 --prover vampire --precompute_arithmetics ./case_data.json
'''

if __name__ == '__main__':
    main()
