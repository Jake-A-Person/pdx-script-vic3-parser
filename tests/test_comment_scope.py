import unittest

from parser.scope import *
from parser.statement import *


class TestCommentScope(unittest.TestCase):
    _scope:Scope
    script = open("../eg_scrip_files/50_sick_us_dtnw.txt", "r", encoding="utf-8-sig", newline="\n")
    _scope = Scope(script.read())
    script.close()

    def test_first_scope(self):
        self.assertEqual(self._scope.get_scopes()[0].get_name(), "je_sick_us")
    def test_second_scope(self):
        self.assertEqual(self._scope.get_scopes()[1].get_name(), "je_sick_us_mexcio")
    def test_2_scope_deep(self):
        self.assertEqual(self._scope.get_scopes()[0].get_scopes()[0].get_name(), "immediate")
        self.assertEqual(len(self._scope.get_scopes()[0].get_scopes()[0].get_statements()),0)
    def test_3_scope_deep(self):
        self.assertEqual(self._scope.get_scopes()[0].get_scopes()[0].get_scopes()[0].get_name(), "set_variable")
        self.assertEqual(len(self._scope.get_scopes()[0].get_scopes()[0].get_scopes()[0].get_statements()),2)
    def test_empty_scope(self):
        self.assertEqual(self._scope.get_scopes()[0].get_scopes()[1].get_name(), "possible")
        self.assertEqual(len(self._scope.get_scopes()[0].get_scopes()[1].get_statements()),0)


if __name__ == '__main__':
    unittest.main()
