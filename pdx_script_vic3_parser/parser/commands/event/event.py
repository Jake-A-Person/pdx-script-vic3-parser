from pdx_script_vic3_parser.parser.commands.scope import Scope
from pdx_script_vic3_parser.parser.util.int_wrap import IntWrap
from pdx_script_vic3_parser.parser.util.util_statement import find_matching_statements
from pdx_script_vic3_parser.parser.util.exceptions import PdxScriptSyntaxError


class Event(Scope):
    """
    Represents a single event in pdx script language.
    A event is in the context of this library is a scope in the highest level of a file of events
    Is a child of the Scope class
    A event can contain any number of Statement objects and any number of Scope objects
    """
    def __init__(self, script: str = "", name: str = "this", operator="=", index: IntWrap = None):
        super().__init__(script, name, operator, index)
        #The values of the statements that will be in events
        self._type:str
        self._hidden:bool
        self._placement:str
        self._title:str
        self._desc:str
        self._flavor:str
        self._duration:str
        #try to find the statements whose property is "type" and operator is "="
        #if it is not present then it is not a valid event so raise an exception
        try:
            self._type = find_matching_statements(self.get_statements(), "type", "=")[0].get_name()
        except IndexError:
            raise PdxScriptSyntaxError(
                f'Event "{self._name}" does not contain a statement defining the event type i.e. "type = country_event"')
        #try to find if there is a statement whose property is "hidden", operator is "=" and vaule is yes
        #if there is one then it is a hidden event meaning some of the statements won't be present
        #if it is not present then it is not a valid event so raise an exception
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
