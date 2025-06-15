from enum import Enum


class Statement(object):
    """
    Represents a pdx script statement.
    A statement is in the context of this library anything in the format:
    property operator value
    i.e. make_independent = yes
    A statement can have any number of: spaces, new lines or tabs separating the property operator and value

    Is used by the Scope
    """
    _property: str
    _value: str

    def __init__(self, property_str: str, value_str: str, operator: str):
        """

        :param property_str: The property (left side) of the pdx script statement
        :type property_str: str
        :param value_str: The value (right side) of the pdx script statement
        :type value_str: str
        :param operator: The operator (sign in the middle) of the pdx script statement
        :type operator: str
        """
        self._property = property_str
        self._value = value_str
        self._operator = operator

    def get_property(self) -> str:
        """

        :return: The property (left side) of the pdx script statement
        :rtype: str
        """
        return self._property

    def get_value(self) -> str:
        """

        :return: The value (right side) of the pdx script statement
        :rtype: str
        """
        return self._value

    def set_property(self, property_str: str) -> None:
        """

        :param property_str: The property (left side) of the pdx script statement
        :type property_str: str
        """
        self._property = property_str

    def set_value(self, value: str) -> None:
        """

        :param value: The value (right side) of the pdx script statement
        :type value: str
        """
        self._value = value

    def set_operator(self, operator: str) -> None:
        """

        :param operator: The operator (sign in the middle) of the pdx script statement
        :type operator: str
        """
        self._operator = operator

    def get_operator(self) -> str:
        """

        :return: The operator (sign in the middle) of the pdx script statement
        :rtype: str
        """
        return self._operator

    def __eq__(self, other):
        #only compare with same type
        if not isinstance(other, Statement):
            return NotImplemented
        else:
            return self._value == other._value and self._property == other._property

    def __str__(self):
        return f"{self._property} {self._operator} {self._value}"
