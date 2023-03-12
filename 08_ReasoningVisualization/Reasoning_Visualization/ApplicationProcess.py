from typing import List
import zipfile
import os
import io
from .NamedFile import NamedFile


class ApplicationProcess:
    metadata_filename = "metadata"
    axioms_folder = "axioms"

    def __init__(self, axiom_files: List[NamedFile]):
        self.axiom_files = axiom_files

    def serialize(self) -> bytes:
        metadata_file = ""
        for axiom_file in self.axiom_files:
            metadata_file += axiom_file.name + "\n"
        with io.BytesIO() as fi:
            with zipfile.ZipFile(fi, 'a', zipfile.ZIP_DEFLATED, False) as zf:
                zf.writestr(ApplicationProcess.metadata_filename, metadata_file.encode('utf-8'))
                for axiom_file in self.axiom_files:
                    filepath = os.path.join(ApplicationProcess.axioms_folder, axiom_file.name)
                    filecontent = axiom_file.content.encode('utf-8')
                    zf.writestr(filepath, filecontent)
            result = fi.getvalue()
            return result

    @staticmethod
    def deserialize(data: bytes) -> 'ApplicationProcess':
        axiom_files = []

        with zipfile.ZipFile(io.BytesIO(data), 'r') as zf:
            namelist = zf.namelist()

            if ApplicationProcess.metadata_filename not in namelist:
                raise Exception("Application process file has no " + ApplicationProcess.metadata_filename)

            metadata_bytes = zf.read(ApplicationProcess.metadata_filename)
            metadata_lines = [x for x in metadata_bytes.split(b'\n') if x]

            for metadata_line in metadata_lines:
                filename = metadata_line.decode('utf-8')
                filepath = os.path.join(ApplicationProcess.axioms_folder, filename)
                if filepath not in namelist:
                    raise Exception("Application process has no declared axiom file " + filepath)
                axiom_content = zf.read(filepath)
                axiom_files.append(NamedFile(filename, axiom_content.decode('utf-8')))

        result = ApplicationProcess(axiom_files)
        return result
