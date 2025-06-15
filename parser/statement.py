class Statement(object):
    _property: str
    _value: str
    def __init__(self, property_str:str, value_str:str):
        self._property = property_str
        self._value = value_str
    def get_property(self):
        return self._property
    def get_value(self):
        return self._value

    def set_property(self, property_str:str):
        self._property = property_str

    def set_value(self, value:str):
        self._value = value

    def __eq__(self,other):
        #only compare with same type
        if not isinstance(other, Statement):
            return NotImplemented
        else:
            return self._value == other._value and self._property == other._property

    def __str__(self):
        return f"{self._property} = {self._value}"