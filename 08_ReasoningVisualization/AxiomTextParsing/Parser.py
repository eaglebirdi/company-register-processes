from typing import List
from .DataStructures import TFFAnnotated
from .RawToBracedConverter import RawToBracedConverter
from .Braced2DictConverter import Braced2DictConverter
from .Dict2StructuresConverter import Dict2StructuresConverter


class Parser:
    def __init__(self):
        pass

    def parse(self, tff_string: str) -> List[TFFAnnotated]:
        # This pipeline is a bit messy and unclean but does the job to exploit
        # the scala implementation of the LEO-III parser via Python.

        converter_raw2braced = RawToBracedConverter()
        braced = converter_raw2braced.convert(tff_string)

        converter_braced2dict = Braced2DictConverter()
        dictionary = converter_braced2dict.convert(braced)

        converter_dict2structures = Dict2StructuresConverter()
        statements: List[TFFAnnotated] = converter_dict2structures.convert(dictionary)
        return statements
