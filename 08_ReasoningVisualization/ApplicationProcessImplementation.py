from typing import Callable
import os
from CaseAxiomGeneration import IGenerator, Configuration


class ApplicationProcessImplementation:
    def __init__(self, gustavus_key: str, name: str,
                 case_axiom_generator_retrieval: Callable[[Configuration], IGenerator]):
        self.gustavus_key = gustavus_key
        self.name = name
        self.combined_key = gustavus_key + "_" + name
        self.case_axiom_generator_retrieval = case_axiom_generator_retrieval
        self.root_rule = "is_application_legal"

    def get_package_path(self):
        folder_path = self._get_package_folder_path()
        return os.path.join(folder_path, self.combined_key + ".zip")

    def get_package_path_without_arithmetic(self):
        folder_path = self._get_package_folder_path()
        return os.path.join(folder_path, self.combined_key + "_noarith.zip")

    def _get_package_folder_path(self) -> str:
        this_path = os.path.dirname(__file__)
        return os.path.join(this_path, "ApplicationProcesses", self.combined_key)
