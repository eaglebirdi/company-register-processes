from typing import List
import argparse
import os
from ReasoningVisualization import Executor, ApplicationProcess
from ReasoningVisualization import InputData, NamedFile
from ReasoningVisualization import IProverTool, Cvc5Prover, KorovinProver, Leo3Prover, PrincessProver, VampireProver


def get_prover_tool(name: str, timeout: int) -> IProverTool:
    if name.lower() == 'cvc5':
        return Cvc5Prover(timeout)
    elif name.lower() == 'iprover' or name.lower() == 'korovin':
        return KorovinProver(timeout)
    elif name.lower() == 'leo3' or name.lower() == 'leo-iii':
        return Leo3Prover(timeout)
    elif name.lower() == 'princess':
        return PrincessProver(timeout)
    elif name.lower() == 'vampire':
        return VampireProver(timeout)
    else:
        raise Exception("The prover '" + name + "' does not exist.")


def execute(application_process_data: bytes, case_axioms: List[NamedFile],
            prover: str, timeout: int, root_rule: str, main_object: str,
            single_file_axioms: bool):
    prover_tool = get_prover_tool(prover, timeout)

    application_process = ApplicationProcess.deserialize(application_process_data)

    input_data = InputData(application_process.axiom_files,
                           case_axioms,
                           root_rule,
                           main_object,
                           prover_tool,
                           single_file_axioms)

    executor = Executor(input_data)
    executor.execute()
    executor.print()


def main():
    parser = argparse.ArgumentParser("Visualize reasoning for company register application process")
    parser.add_argument("--process_file", required=True, help="Name of the application process file")
    parser.add_argument("--prover", required=True, help="Name of the ATP tool. Allowed values: cvc5, iprover, leo3, princess, vampire")
    parser.add_argument("--timeout", default=3, help="Timeout in seconds for each prover invocation")
    parser.add_argument("--root_rule", required=True, help="Name of the root rule predicate")
    parser.add_argument("--main_object", required=True, help="Name of the main object to which the root rule is applied")
    parser.add_argument("--single_file_axioms", action='store_true', help="Whether the axioms are merged into one single file")
    parser.add_argument("case_axiom_files", nargs='+', help="Names of the case axiom files")

    args = parser.parse_args()

    with open(args.process_file, 'rb') as fi:
        application_prcess_data = fi.read()

    case_axioms = []
    for case_axiom_filepath in args.case_axiom_files:
        with open(case_axiom_filepath, 'r') as fi:
            _, case_axiom_filename = os.path.split(case_axiom_filepath)
            case_axiom_filecontent = fi.read()
            case_axioms.append(NamedFile(case_axiom_filename, case_axiom_filecontent))

    execute(application_prcess_data, case_axioms,
            args.prover, args.timeout,
            args.root_rule, args.main_object,
            args.single_file_axioms)


if __name__ == '__main__':
    main()
