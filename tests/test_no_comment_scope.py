import unittest
from parser.scope import *
from parser.statement import *



class TestNoCommentScope(unittest.TestCase):
    _scope: Scope
    def setUp(self):
        script = open("../eg _scrip_files/no_comments_scope_simple.txt", "r", encoding="utf-8-sig", newline="\n")
        self._scope = Scope(script.read())
    def test_first_scope(self):
        self.assertEqual(self._scope.get_scopes()[0].get_name(), "je_sick_us")  # add assertion here


if __name__ == '__main__':
    unittest.main()
