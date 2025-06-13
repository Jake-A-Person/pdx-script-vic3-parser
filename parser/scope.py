from .statement import Statement

class Scope(object):
    _name: str
    _statements: list[Statement] = list()
    _script: str
    _index:int
    def __init__(self, script: str,index:int = 0, name:str = "this"):
        self._script = script
        self._index = index
        self._name = name
        self.parse_space_start_exp()
    def start_search(self):
        pass
        # while self._index < len(self._script):
        #     if self._script[self._index] == " " or self._script[self._index] == "\n":
        #         self._index += 1
        #         continue
        #     elif self._script[self._index] == :
    def parse_space_start_exp(self):
        while self._index < len(self._script):
            #if this char is a space or new line then go to next char
            #if expression hasn't started yet
            if self._script[self._index] == " " or self._script[self._index] == "\n":
                self._index += 1
            elif self._script[self._index] == "}":
                #TODO change scope
                self._index += 1
            else:
                self.parse_start_exp()
    def parse_start_exp(self):
        property_str: str = ""
        while self._index < len(self._script):
            #if this char is a space or new line or = then go to next char
            #if left side of the expression has finished
            if self._script[self._index] == " " or self._script[self._index] == "\n" or self._script[self._index] == "=":
               self.parse_space_mid_exp(property_str)
               break
            else:
                property_str += self._script[self._index]
                self._index += 1
    def parse_space_mid_exp(self,property_str:str):
        while self._index < len(self._script):
            #if not the assignment operator loop
            if self._script[self._index] != "=":
                self._index += 1
            else:
                self._index += 1
                break
        while self._index < len(self._script):
            if self._script[self._index] == " " or self._script[self._index] == "\n":
                self._index += 1
            else:
                self.parse_end_exp(property_str)
                break
    def parse_end_exp(self,property_str:str):
        if self._script[self._index] == "{":
            #TODO change scope
            self._index += 1
        else:
            value: str = ""
            while self._index < len(self._script):
                if self._script[self._index] == " " or self._script[self._index] == "\n":
                    stat = Statement(property_str,value)
                    self._statements.append(stat)
                    self._index += 1
                    break
                else:
                    value += self._script[self._index]
                    self._index += 1

    def get_statements(self) -> list[Statement]:
        return self._statements
    def get_name(self) -> str:
        return self._name

    def __str__(self):
        str1 = [str(i) for i in self._statements]
        #puts each of the statements on to a new line
        str2 = "\n".join(str1)
        return str(str2) + "\n" + str(len(self._statements))