class TypedVariable:
    def __init__(self, variable_name: str, variable_type: str):
        self.variable_name = variable_name
        self.variable_type = variable_type

    def __str__(self):
        return self.variable_name + ": " + self.variable_type
