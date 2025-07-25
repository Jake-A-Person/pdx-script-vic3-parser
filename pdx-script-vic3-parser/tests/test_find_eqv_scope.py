import unittest
from parser.commands.scope import *

class TestFindEqvScope(unittest.TestCase):
    _scope:Scope
    script = open("eg_scrip_files/50_sick_us_dtnw.txt", "r", encoding="utf-8-sig", newline="\n")
    _scope = Scope(script.read())
    script.close()

    def test_top_level_all_stat(self):
        eqv_scope = Scope("", name="je_sick_us")
        eqv_scope.add_statement(Statement("icon","\"gfx/interface/icons/event_icons/event_election.dds\"","="))
        eqv_scope.add_statement(Statement("group", "je_group_internal_affairs", "="))
        eqv_scope.add_statement(Statement("progressbar", "yes", "="))
        eqv_scope.add_statement(Statement("weight", "10000", "="))
        target_scope = self._scope.get_scopes()[0]
        self.assertEqual(self._scope.find_eqv_scope(eqv_scope), target_scope)  # add assertion here
    def test_top_level_some_stat(self):
        eqv_scope = Scope("", name="je_sick_us")
        eqv_scope.add_statement(Statement("progressbar", "yes", "="))
        target_scope = self._scope.get_scopes()[0]
        self.assertEqual(self._scope.find_eqv_scope(eqv_scope), target_scope)  # add assertion here
    def test_top_level_second(self):
        eqv_scope = Scope("", name="je_sick_us_mexcio")
        eqv_scope.add_statement(Statement("group", "je_group_internal_affairs", "="))
        target_scope = self._scope.get_scopes()[1]
        self.assertEqual(self._scope.find_eqv_scope(eqv_scope), target_scope)  # add assertion here
    def test_second_level(self):
        eqv_scope = Scope("", name="c:MIS")
        eqv_scope.add_statement(Statement("remove_modifier", "union_with_mexico", "="))
        target_scope = self._scope.get_scopes()[1].get_scopes()[5].get_scopes()[3]
        self.assertEqual(self._scope.find_eqv_scope(eqv_scope), target_scope,str(eqv_scope) + "!= \n" + str(target_scope))

if __name__ == '__main__':
    unittest.main()
