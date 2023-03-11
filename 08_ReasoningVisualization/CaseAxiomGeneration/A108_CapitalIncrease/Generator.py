from typing import List
from Reasoning_Visualization import NamedFile
from ..Configuration import Configuration
from ..IGenerator import IGenerator
from ..GenerationResult import GenerationResult
from ..Helpers.CaseFactHelper import *
from ..Helpers.InstanceHelper import *
from ..Helpers.GeneralHelper import is_empty
from .NamingHelper import *

newline = Configuration.newline


class Generator(IGenerator):
    def __init__(self):
        super().__init__()

    def create(self, input_data: dict, root_rule: str) -> GenerationResult:
        self._validate(input_data, __file__)

        axiom_files = [
            NamedFile("instances.ax", self._create_instances_axioms(input_data)),
            NamedFile("casefacts.ax", self._create_casefacts_axioms(input_data))
        ]
        main_object_name = self._get_main_object_name(root_rule)

        result = GenerationResult(axiom_files, main_object_name, root_rule)
        return result

    def _create_instances_axioms(self, input_data: dict) -> str:
        pass

    def _create_casefacts_axioms(self, input_data: dict) -> str:
        pass

    def _get_main_object_name(self, root_rule: str) -> str:
        if root_rule == "is_application_legal":
            return get_cname_application()

        raise Exception("no implementation provided for root rule " + root_rule)

