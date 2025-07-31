from abc import ABC 
class Command(ABC):
    def __init__(self, name: str, operator: str):
        self._name = name
        self._operator = operator

    def get_name(self) -> str:
        """

        :return: The value (right side) of the pdx script statement
        :rtype: str
        """
        return self._name

    def get_operator(self) -> str:
        """

        :return: The operator (sign in the middle) of the pdx script statement
        :rtype: str
        """
        return self._operator

    def to_pdx_script(self) -> str:
        pass