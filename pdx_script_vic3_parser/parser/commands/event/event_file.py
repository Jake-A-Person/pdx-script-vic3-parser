from pdx_script_vic3_parser.parser.commands.scope import Scope
from pdx_script_vic3_parser.parser.util.int_wrap import IntWrap
from pdx_script_vic3_parser.parser.commands.event.event import Event
from pdx_script_vic3_parser.parser.util.util_statement import find_matching_statements

class EventFile(Scope):
    def __init__(self, script: str = "", name: str = "this", operator="=", index: IntWrap = None):
        super().__init__(script, name, operator ,index)
        namespace = find_matching_statements(self.get_statements(),"namespace","=")
        if len(namespace) != 0:
            self._name = namespace[0].get_value()


    def _go_to_next_scope(self, next_scope_name: str, next_scope_operator: str):
        self._commands.append(Event(self._script, next_scope_name, next_scope_operator , self._index))
