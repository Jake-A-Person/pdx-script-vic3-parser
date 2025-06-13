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
    def __str__(self):
        return f"{{{self._property} : {self._value}}}"