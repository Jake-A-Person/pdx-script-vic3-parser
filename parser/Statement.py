class Statement:
    _name = ""
    _value = ""
    def __init__(self, name, value):
        _name = name
        _value = value
    def get_name(self):
        return self._name
    def get_value(self):
        return self._name