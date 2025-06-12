import Statement

class Scope:
    _name: str
    _statements: set = set
    _script: str
    _index:int
    def __init__(self, script: str,index:int = 0, name:str = "this"):
        self._script = script
        self._index = index
        self._name = name
        self.start_search()
    def start_search(self):
        print(self._script)