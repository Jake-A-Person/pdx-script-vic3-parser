from parser.scope import Scope
from parser.int_wrap import IntWrap
from parser.event.event import Event
from parser.statement_list_search import find_matching_statements

class EventFile(Scope):
    def __init__(self, script: str, index:IntWrap = None, name:str = "this"):
        super().__init__(script, index,name)
        namespace = find_matching_statements(self.get_statements(),"namespace","=")
        if len(namespace) != 0:
            self._name = namespace[0].get_value()


    def _go_to_next_scope(self, next_scope_name: str):
        self._scopes.append(Event(self._script, self._index, next_scope_name))
