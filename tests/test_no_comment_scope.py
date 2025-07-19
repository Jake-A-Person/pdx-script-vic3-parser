import unittest
from parser.commands.scope import *

class TestNoCommentScope(unittest.TestCase):
    scope1:Scope
    script = open("../eg_scrip_files/no_comments_50_sick_us_dtnw.txt", "r", encoding="utf-8-sig", newline="\n")
    scope1 = Scope(script.read())
    script.close()

    def test_first_scope(self):
        self.assertEqual(self.scope1.get_scopes()[0].get_name(), "je_sick_us")
    def test_second_scope(self):
        self.assertEqual(self.scope1.get_scopes()[1].get_name(), "je_sick_us_mexcio")
    def test_2_scope_deep(self):
        self.assertEqual(self.scope1.get_scopes()[0].get_scopes()[0].get_name(), "immediate")
        self.assertEqual(len(self.scope1.get_scopes()[0].get_scopes()[0].get_statements()),0)
    def test_3_scope_deep(self):
        self.assertEqual(self.scope1.get_scopes()[0].get_scopes()[0].get_scopes()[0].get_name(), "set_variable")
        self.assertEqual(len(self.scope1.get_scopes()[0].get_scopes()[0].get_scopes()[0].get_statements()),2)
    def test_empty_scope(self):
        self.assertEqual(self.scope1.get_scopes()[0].get_scopes()[1].get_name(), "possible")
        self.assertEqual(len(self.scope1.get_scopes()[0].get_scopes()[1].get_statements()),0)



if __name__ == '__main__':
    unittest.main()
