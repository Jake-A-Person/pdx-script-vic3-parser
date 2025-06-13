import unittest
from parser.scope import *
from parser.statement import *



class TestNoCommentScope(unittest.TestCase):
    scope1:Scope
    script = open("../eg _scrip_files/no_comments_scope_simple.txt", "r", encoding="utf-8-sig", newline="\n")
    scope1 = Scope(script.read())
    script.close()

    def test_first_scope(self):
        self.assertEqual(self.scope1.get_scopes()[0].get_name(), "je_sick_us")  # add assertion here
    def test_second_scope(self):
        self.assertEqual(self.scope1.get_scopes()[1].get_name(), "je_hi")  # add assertion here



if __name__ == '__main__':
    unittest.main()
