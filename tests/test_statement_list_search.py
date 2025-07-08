import unittest
from parser.statement import *
from parser.statement_list_search import find_matching_statements


class TestStatementListSearch(unittest.TestCase):
    test_data:list[Statement] = [Statement("type","country_event","="),
    Statement("type","country_event",">="),
    Statement("title","dtnw_sick_us","="),
    Statement("duration","1","=")]

    def test_no_filter(self):
        self.assertEqual(find_matching_statements(self.test_data), self.test_data)


if __name__ == '__main__':
    unittest.main()
