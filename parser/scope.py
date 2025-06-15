from os import linesep as os_linesep
from copy import copy

from .statement import Statement

class IntWrap(object):
    """
    A wrapper for an int
    Used in Scope class to allow for ints to be passed by reference
    """
    def __init__(self, val):
        self.val = val

class Scope(object):
    """
    Represents a pdx script scope.
    A statement is in the context of this library anything in the format:
    name = {.
    A statement can have any number of: spaces, new lines or tabs separating the name = and {.
    The scope is closed by a }.
    A scope can contain any number of Statement objects and any number of Scope objects
    """
    def __init__(self, script: str, index:IntWrap = None, name:str = "this"):
        """
        Parses the given script when the object is created and creates Scopes and statements based on the given script

        :param script: The pdx script to parse, must be LF
        :type script: str
        :param index: The index of the pdx script to parse will default to a new IntWrap(0)
        :type index: IntWrap
        :param name: Name of this scope
        :type name: str
        """
        self._script = script
        #if no index is given then default to 0
        self._index = index if index is not None else IntWrap(0)
        self._name = name
        self._statements = list()
        self._scopes = list()
        self.__parse_space_start_exp()

    def __parse_space_start_exp(self):
        while self._index.val < len(self._script):
            self.__check_for_comment()
            #if this char is a space or new line then go to next char
            #if expression hasn't started yet
            if self._script[self._index.val] == " " or self._script[self._index.val] == "\n" or self._script[self._index.val] == "\t":
                self._index.val += 1
            elif self._script[self._index.val] == "}":
                #change scope
                self._index.val += 1
                return
            else:
                self.__parse_start_exp()

    def __parse_start_exp(self):
        property_str: str = ""
        while self._index.val < len(self._script):
            self.__check_for_comment()
            #if this char is a space or new line or = then go to next char
            #if left side of the expression has finished
            if self._script[self._index.val] == " " or self._script[self._index.val] == "\n" or self._script[self._index.val] == "=":
               #parse the assignment operator
               self.__parse_space_mid_exp(property_str)
               #go back to parse_space_start_exp
               return
            else:
                #add the current char on to the name of the property (left side of the statement)
                property_str += self._script[self._index.val]
                self._index.val += 1

    def __parse_space_mid_exp(self, property_str:str):
        operator: str = ""
        #looping to the assignment from the left
        while self._index.val < len(self._script):
            self.__check_for_comment()
            #if not the assignment operator loop
            if self._script[self._index.val] != "=" and self._script[self._index.val] != ">" and self._script[self._index.val] != "<":
                self._index.val += 1
                operator = self._script[self._index.val]
            else:
                if (self._script[self._index.val] == ">" or self._script[self._index.val] == "<") and self._script[self._index.val+1] == "=":
                    self._index.val += 1
                    operator += self._script[self._index.val]
                # if it is the assignment operator go to the next char and exit the loop
                self._index.val += 1
                break
        # looping to the value or scope operator ({) from the operator
        while self._index.val < len(self._script):
            self.__check_for_comment()
            #if it is not par of the value or a scope operator ({) no to next char
            if self._script[self._index.val] == " " or self._script[self._index.val] == "\n" or self._script[self._index.val] == "\t":
                self._index.val += 1
            else:
                self.__parse_end_exp(property_str, operator)
                #go back to parse_start_exp which goes back to parse_space_start_exp
                return

    def __parse_end_exp(self, property_str:str, operator:str):
        #if it is the scope operator ({) change scope
        if self._script[self._index.val] == "{":
            self._index.val += 1
            self._scopes.append(Scope(self._script,self._index,property_str))
            return
        else:
            #is a value so parse it
            value: str = ""
            while self._index.val < len(self._script):
                self.__check_for_comment()
                #if it is the end if the value
                if self._script[self._index.val] == " " or self._script[self._index.val] == "\n" or self._script[self._index.val] == "\t":
                    #create a new statement using the property and value parsed and it to the list fo statements
                    stat = Statement(property_str,value,operator)
                    self._statements.append(stat)
                    self._index.val += 1
                    # go back to parse_start_exp which goes back to parse_space_start_exp
                    return
                #if it is closing the current scope
                if self._script[self._index.val] == "}":
                    stat = Statement(property_str,value,operator)
                    self._statements.append(stat)
                    return
                else:
                    value += self._script[self._index.val]
                    self._index.val += 1

    def __check_for_comment(self):
        #if it is the start of a comment
        if self._script[self._index.val] == "#":
            #loop until the end of the comment
            while self._index.val < len(self._script) and self._script[self._index.val] != "\n":
                self._index.val += 1

    def get_statements(self) -> list[Statement]:
        """

        :return: The list of statements in the current scope
        :rtype: list[Statement]
        """
        return self._statements

    def get_name(self) -> str:
        """

        :return: The name of the current scope
        :rtype: str
        """
        return self._name

    def get_scopes(self) -> list:
        """

        :return: The list of scopes in the current scope
        :rtype: list[Scope]
        """
        return self._scopes

    def add_statement(self, stat: Statement):
        """

        :param stat: The statement to add
        :type stat: Statement
        """
        self._scopes.append(stat)

    def remove_statement(self, stat: Statement):
        """

        :param stat: The statement to remove
        :type stat: Statement
        :raises: ValueError
        """
        self._scopes.remove(stat)

    def add_scope(self, scope):
        """

        :param scope: The scope to add
        :type scope: Scope
        """
        self._scopes.append(scope)

    def remove_scope(self, scope):
        """

        :param scope: The scope to remove
        :type scope: Scope
        :raises: ValueError
        """

        self._scopes.remove(scope)

    def to_pdx_script(self, indent_char:str="\t", new_line_char:str="\n", indentation_level:int = 0 ) -> str:
        """
        Translates the scope into valid pdx script

        :param indent_char: The character used to indent the pdx script by default \t
        :type indent_char: str
        :param new_line_char: The character used to show a new line in the pdx script by default \n
        :type new_line_char: str
        :param indentation_level: The level of the pdx script by default 0
        :type indentation_level: int
        :return: A string containing the Scope in valid pdx script
        :rtype: str
        """
        return_str:str = indent_char*indentation_level + self._name + " = {" + new_line_char
        for stat in self._statements:
            return_str += (indentation_level+1)*indent_char + str(stat) + new_line_char
        for scope in self._scopes:
            return_str += scope.to_pdx_script(indentation_level=indentation_level + 1) + new_line_char
        return return_str + indent_char*indentation_level + "}"

    def __str__(self):
        return self.to_pdx_script("   ",os_linesep)