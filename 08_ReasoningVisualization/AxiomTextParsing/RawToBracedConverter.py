import os
import subprocess
import uuid


class RawToBracedConverter:
    def __init__(self):
        this_path = os.path.dirname(__file__)
        self.tptp_parser_tool_path = os.path.join(this_path, "tptp-parser-tool.jar")
        self.fail_message = "Failed to retrieve output from tptp-parser-tool"

    def convert(self, tptp_string: str) -> str:
        filename = self._create_tptp_file(tptp_string)
        pipe = subprocess.Popen([
            "java",
            "-jar",
            self.tptp_parser_tool_path,
            "-i",
            filename
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = pipe.communicate()
        output = out.decode('utf-8')
        error = err.decode('utf-8')

        if error != '':
            if "LinkageError occurred while loading" in err.decode('utf-8'):
                raise Exception(self.fail_message + ": Java linkage error. Update of java runtime is required.")
            else:
                raise Exception(self.fail_message + ": " + error)

        self._delete_tptp_file(filename)

        if output is None or output == '':
            raise Exception(self.fail_message + ": no output")

        if output.startswith("Unhandled exception"):
            raise Exception(self.fail_message + ": " + output)

        return output

    def _create_tptp_file(self, tptp_string):
        filename = "_AAA_" + uuid.uuid4().hex + ".txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(tptp_string)
        return filename

    def _delete_tptp_file(self, filename):
        os.remove(filename)
