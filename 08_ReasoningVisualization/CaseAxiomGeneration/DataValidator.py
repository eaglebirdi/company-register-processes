import json
import jsonschema
from .ValidationResult import ValidationResult


class DataValidator:
    def __init__(self, schema_path: str):
        self.schema_path = schema_path

    def validate(self, data_json: object) -> ValidationResult:
        schema = self._load_schema()
        try:
            jsonschema.validate(instance=data_json, schema=schema)
            return ValidationResult(True, "")
        except jsonschema.exceptions.ValidationError as err:
            return ValidationResult(False, err.message)

    def _load_schema(self):
        with open(self.schema_path, 'r') as f:
            schema_json = json.load(f)
        return schema_json
