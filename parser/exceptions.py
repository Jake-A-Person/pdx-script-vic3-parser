
class PdxScriptSyntaxError(Exception):
    def __init__(self, message="Invalid paradox script syntax"):
        self.message = message