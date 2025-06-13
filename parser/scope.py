from .statement import Statement

class int_wrap(object):
    val: int
    def __init__(self, val):
        self.val = val

class Scope(object):
    _name: str
    _statements: list[Statement] = list()
    _script: str
    _scopes: list = list()
    _index:int_wrap
    def __init__(self, script: str,index:int_wrap = int_wrap(0), name:str = "this"):
        self._script = script
        self._index = index
        self._name = name
        self.parse_space_start_exp()

    def parse_space_start_exp(self):
        while self._index.val < len(self._script):
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
            #if not the assignment operator loop
            if self._script[self._index.val] != "=":
                self._index.val += 1
            else:
                #if it is the assignment operator go to the next char and exit the loop
                self._index.val += 1
                break
        # looping to the value or scope operator ({) from the operator
        while self._index.val < len(self._script):
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
            #TODO change scope
            self._index.val += 1
            self._scopes.append(Scope(self._script,self._index,property_str))
            return
        else:
            #is a value so parse it
            value: str = ""
            while self._index.val < len(self._script):
                #if it is the end if the value
                if self._script[self._index.val] == " " or self._script[self._index.val] == "\n" or self._script[self._index.val] == "\t":
                    #create a new statement using the property and value parsed and it to the list fo statements
                    stat = Statement(property_str,value)
                    self._statements.append(stat)
                    self._index.val += 1
                    # go back to parse_start_exp which goes back to parse_space_start_exp
                    return
                else:
                    value += self._script[self._index.val]
                    self._index.val += 1

    def get_statements(self) -> list[Statement]:
        return self._statements

    def get_name(self) -> str:
        return self._name

    def __str__(self):
        str1 = [str(i) for i in self._statements]
        #puts each of the statements on to a new line
        str2 = "\n".join(str1)
        return str(str2) + "\n" + str(len(self._statements))