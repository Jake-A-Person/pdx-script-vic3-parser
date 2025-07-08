from parser.scope import Scope
from parser.int_wrap import IntWrap
import parser.statement_list_search
from parser.statement import Statement
from parser.statement_list_search import find_matching_statements
from parser.exceptions import PdxScriptSyntaxError


class Event(Scope):
    def __init__(self, script: str, index:IntWrap = None, name:str = "this"):
        super().__init__(script, index,name)
        self._type:str
        self._hidden:bool
        self._placement:str
        self._title:str
        self._desc:str
        self._flavor:str
        self._duration:str
        try:
            self._type = find_matching_statements(self.get_statements(), "type", "=")[0].get_value()
        except IndexError:
            raise PdxScriptSyntaxError(
                f'Event "{self._name}" does not contain a statement defining the event type i.e. "type = country_event"')

        if len(find_matching_statements(self.get_statements(),"hidden","=","yes")) > 0:
            self._hidden = True
        else:
            self._hidden = False
            try:
                self._placement = find_matching_statements(self.get_statements(),"placement","=")[0].get_value()
                self._title = find_matching_statements(self.get_statements(),"title","=")[0].get_value()
                self._desc = find_matching_statements(self.get_statements(),"desc","=")[0].get_value()
                self._flavor = find_matching_statements(self.get_statements(),"flavor","=")[0].get_value()
                self._duration  = find_matching_statements(self.get_statements(),"flavor","=")[0].get_value()
            except IndexError:
                raise PdxScriptSyntaxError(f'Event "{self._name}" is not a hidden event and does not contain all the necessary statements')
