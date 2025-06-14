from os import linesep as os_linesep
from copy import copy

from .statement import Statement

class IntWrap(object):
    def __init__(self, val):
        self.val = val

class Scope(object):
    def __init__(self, script: str, index:IntWrap = None, name:str = "this"):
        self._script = script
        #if no index is given then default to 0
        self._index = index if index is not None else IntWrap(0)
        self._name = name
        self._statements = list()
        self._scopes = list()
        self.parse_space_start_exp()

    def parse_space_start_exp(self):
        while self._index.val < len(self._script):
            self.check_for_comment()
            #if this char is a space or new line then go to next char
            #if expression hasn't started yet
            if self._script[self._index.val] == " " or self._script[self._index.val] == "\n" or self._script[self._index.val] == "\t":
                self._index.val += 1
            elif self._script[self._index.val] == "}":
                #change scope
                self._index.val += 1
                return
            else:
                self.parse_start_exp()

    def parse_start_exp(self):
        property_str: str = ""
        while self._index.val < len(self._script):
            self.check_for_comment()
            #if this char is a space or new line or = then go to next char
            #if left side of the expression has finished
            if self._script[self._index.val] == " " or self._script[self._index.val] == "\n" or self._script[self._index.val] == "=":
               #parse the assignment operator
               self.parse_space_mid_exp(property_str)
               #go back to parse_space_start_exp
               return
            else:
                #add the current char on to the name of the property (left side of the statement)
                property_str += self._script[self._index.val]
                self._index.val += 1

    def parse_space_mid_exp(self,property_str:str):
        #looping to the assignment from the left
        while self._index.val < len(self._script):
            self.check_for_comment()
            #if not the assignment operator loop
            if self._script[self._index.val] != "=":
                self._index.val += 1
            else:
                #if it is the assignment operator go to the next char and exit the loop
                self._index.val += 1
                break
        # looping to the value or scope operator ({) from the operator
        while self._index.val < len(self._script):
            self.check_for_comment()
            #if it is not par of the value or a scope operator ({) no to next char
            if self._script[self._index.val] == " " or self._script[self._index.val] == "\n" or self._script[self._index.val] == "\t":
                self._index.val += 1
            else:
                self.parse_end_exp(property_str)
                #go back to parse_start_exp which goes back to parse_space_start_exp
                return

    def parse_end_exp(self,property_str:str):
        #if it is the scope operator ({) change scope
        if self._script[self._index.val] == "{":
            self._index.val += 1
            self._scopes.append(Scope(self._script,self._index,property_str))
            return
        else:
            #is a value so parse it
            value: str = ""
            while self._index.val < len(self._script):
                self.check_for_comment()
                #if it is the end if the value
                if self._script[self._index.val] == " " or self._script[self._index.val] == "\n" or self._script[self._index.val] == "\t":
                    #create a new statement using the property and value parsed and it to the list fo statements
                    stat = Statement(property_str,value)
                    self._statements.append(stat)
                    self._index.val += 1
                    # go back to parse_start_exp which goes back to parse_space_start_exp
                    return
                #if it is closing the current scope
                if self._script[self._index.val] == "}":
                    stat = Statement(property_str,value)
                    self._statements.append(stat)
                    return
                else:
                    value += self._script[self._index.val]
                    self._index.val += 1

    def check_for_comment(self):
        #if it is the start of a comment
        if self._script[self._index.val] == "#":
            #loop until the end of the comment
            while self._index.val < len(self._script) and self._script[self._index.val] != "\n":
                self._index.val += 1

    def get_statements(self) -> list[Statement]:
        return self._statements

    def get_name(self) -> str:
        return self._name

    def get_scopes(self) -> list:
        return self._scopes

    def to_pdx_script(self, indent_char:str="\t", new_line_char:str="\n", indentation_level:int = 0 ) -> str:
        return_str:str = indent_char*indentation_level + self._name + " = {" + new_line_char
        for stat in self._statements:
            return_str += (indentation_level+1)*indent_char + str(stat) + new_line_char
        for scope in self._scopes:
            return_str += scope.to_pdx_script(indentation_level=indentation_level + 1) + new_line_char
        return return_str + indent_char*indentation_level + "}"
        #for scope in self._scopes:


    def __str__(self):
        return self.to_pdx_script("   ",os_linesep)