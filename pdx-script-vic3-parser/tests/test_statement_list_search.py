import unittest
from parser.util.util_statement import *


class TestStatementListSearch(unittest.TestCase):
    test_data:list[Statement] = [Statement("type","country_event","="),
    Statement("type","country_event",">="),
    Statement("title","dtnw_sick_us","="),
    Statement("duration","1","=")]

    def test_no_filter(self):
        self.assertEqual(find_matching_statements(self.test_data), self.test_data)
    def test_eql_operators(self):
        self.assertEqual(find_matching_statements(self.test_data,operator="="), [self.test_data[0],self.test_data[2],self.test_data[3]])
    def test_les_eql_operators(self):
        self.assertEqual(find_matching_statements(self.test_data,operator=">="), [self.test_data[1]])
    def test_same_property(self):
        self.assertEqual(find_matching_statements(self.test_data,"type"), self.test_data[0:2])
    def test_one_property(self):
        self.assertEqual(find_matching_statements(self.test_data,"duration"), [self.test_data[3]])
    def test_same_value(self):
        self.assertEqual(find_matching_statements(self.test_data,value="country_event"), self.test_data[0:2])
    def test_one_value(self):
        self.assertEqual(find_matching_statements(self.test_data,value="1"), [self.test_data[3]])
    def test_property_operator(self):
        self.assertEqual(find_matching_statements(self.test_data,"type","="), [self.test_data[0]])
    def test_invalid_value(self):
        self.assertEqual(find_matching_statements(self.test_data, value = "2"), [])
    def test_invalid_property(self):
        self.assertEqual(find_matching_statements(self.test_data,"t1tle"), [])
    def test_invalid_operator(self):
        self.assertEqual(find_matching_statements(self.test_data,"890"), [])

if __name__ == '__main__':
    unittest.main()