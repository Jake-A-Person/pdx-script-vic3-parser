from os import linesep as os_linesep

from parser.command import Command
from parser.statement import Statement
from parser.int_wrap import IntWrap


class Scope(Command):
    """
    Represents a pdx script scope.
    A statement is in the context of this library anything in the format:
    name = {.
    A statement can have any number of: spaces, new lines or tabs separating the name = and {.
    The scope is closed by a }.
    A scope can contain any number of Statement objects and any number of Scope objects
    """
    def __init__(self, script: str = "", name: str = "this", operator="=", index: IntWrap = None):
        """
        Parses the given script when the object is created and creates Scopes and statements based on the given script

        :param operator:
        :type operator:
        :param script: The pdx script to parse, must be LF
        :type script: str
        :param index: The index of the pdx script to parse will default to a new IntWrap(0)
        :type index: IntWrap
        :param name: Name of this scope
        :type name: str
        """
        super().__init__(name, operator)
        self._script = script
        #if no index is given then default to 0
        self._index = index if index is not None else IntWrap(0)
        self._commands = list()
        self._commands = list()
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
        #valid operators
        valid_single_op = ["<",">","="]
        valid_multi_op = ["<=",">=","?="]
        #looping to the assignment operator from the left
        while self._index.val < len(self._script):
            self.__check_for_comment()
            #check if the next two chars are a multi char operator
            if (self._index.val < len(self._script) + 1) and (self._script[self._index.val:self._index.val+2] in valid_multi_op):
                #next two chars
                operator = self._script[self._index.val:self._index.val+2]
                self._index.val += 2
                #exit loop
                break
            #check if the next char is a single char operator
            elif self._script[self._index.val] in valid_single_op:
                operator = self._script[self._index.val]
                self._index.val += 1
                #exit loop
                break
            self._index.val += 1
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
            self._go_to_next_scope(property_str,operator)
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
                    self._commands.append(stat)
                    self._index.val += 1
                    # go back to parse_start_exp which goes back to parse_space_start_exp
                    return
                #if it is closing the current scope
                if self._script[self._index.val] == "}":
                    stat = Statement(property_str,value,operator)
                    self._commands.append(stat)
                    return
                else:
                    value += self._script[self._index.val]
                    self._index.val += 1

    def _go_to_next_scope(self, next_scope_name:str, next_scope_operator:str):
        self._commands.append(Scope(self._script, next_scope_name, next_scope_operator, self._index))

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
        statements: list[Statement] = []
        for command in self._commands:
            if type(command) == Statement:
                statements.append(command)

        return statements

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
        scopes: list[Scope] = []
        for command in self._commands:
            if type(command) == Scope:
                scopes.append(command)
        return scopes

    def add_statement(self, stat: Statement):
        """

        :param stat: The statement to add
        :type stat: Statement
        """
        self._commands.append(stat)

    def remove_statement(self, stat: Statement):
        """

        :param stat: The statement to remove
        :type stat: Statement
        :raises: ValueError
        """
        self._commands.remove(stat)

    def add_scope(self, scope):
        """

        :param scope: The scope to add
        :type scope: Scope
        """
        self._commands.append(scope)

    def remove_scope(self, scope):
        """

        :param scope: The scope to remove
        :type scope: Scope
        :raises: ValueError
        """

        self._commands.remove(scope)

    def find_eqv_scope(self, eqv_scope):
        if self._name == eqv_scope.get_name():
            if len(eqv_scope.get_statements()) == 0 or all(stat in self.get_statements() for stat in eqv_scope.get_statements()):
                return self
        for child_scope in self.get_scopes():
            return_val = child_scope.find_eqv_scope(eqv_scope)
            if return_val is not None:
                return return_val
        return None

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
        for stat in self.get_statements():
            return_str += (indentation_level+1)*indent_char + str(stat) + new_line_char
        for scope in self.get_scopes():
            return_str += scope.to_pdx_script(indentation_level=indentation_level + 1) + new_line_char
        return return_str + indent_char*indentation_level + "}"

    def __eq__(self, other):
        if not isinstance(other, Scope):
            return NotImplemented
        else:
            return self._name == other._name and self._commands == other._commands and self._commands == other._commands

    def __str__(self):
        return self.to_pdx_script("   ",os_linesep)