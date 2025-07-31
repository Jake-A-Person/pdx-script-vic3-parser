import unittest
from pdx_script_vic3_parser.parser.commands.scope import *


class TestNoCommentNoScope(unittest.TestCase):
    _scope:Scope
    script = open("eg_scrip_files/no_scope_change_no_comments.txt", "r", encoding="utf-8-sig", newline="\n")
    _scope = Scope(script.read())
    script.close()

    def test_first_statement(self):
        self.assertEqual(self._scope.get_statements()[0], Statement("icon","\"gfx/interface/icons/event_icons/event_election.dds\"","="))
    def test_sep_new_line(self):
        self.assertEqual(self._scope.get_statements()[1], Statement("group","je_group_internal_affairs","="))
    def test_sep_2new_lines(self):
        self.assertEqual(self._scope.get_statements()[2], Statement("name","sick_us_var","="))
    def test_sep_space(self):
        self.assertEqual(self._scope.get_statements()[3], Statement("value","0","="))
    def test_sep_new_line_space(self):
        self.assertEqual(self._scope.get_statements()[4], Statement("has_technology_researched","pan-nationalism","="),str(self._scope.get_statements()[4]))
    def test_sep_tab(self):
        self.assertEqual(self._scope.get_statements()[5], Statement("text","je_us_failure_tt","="))


if __name__ == '__main__':
    unittest.main()
