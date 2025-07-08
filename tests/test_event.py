from parser.event.event_file import *
from parser.event.event import *
from parser.statement import *

import unittest

class TestCommentScope(unittest.TestCase):
    _scope:EventFile
    script = open("../eg_scrip_files/dtnw_sick_us.txt", "r", encoding="utf-8-sig", newline="\n")
    _scope = EventFile(script.read())
    script.close()

    def test_name_space(self):
        self.assertEqual(self._scope.get_name(), "dtnw_sick_us")
    def test_first_event_type(self):
        self.assertEqual(type(self._scope.get_scopes()[0]),Event)
    def test_first_event_name(self):
        self.assertEqual(self._scope.get_scopes()[0].get_name(), "dtnw_sick_us.1")
    def test_first_event_statements(self):
        #the statements that are in the event
        valid_statements = [Statement("type","country_event","=")
            ,Statement("placement","root","=")
            ,Statement("title","dtnw_sick_us.1.t","=")
            ,Statement("desc", "dtnw_sick_us.1.d", "=")
            ,Statement("flavor","dtnw_sick_us.1.f","=")
            ,Statement("duration","1","=")]
        self.assertEqual(self._scope.get_scopes()[0].get_statements(),valid_statements)
    # def test_second_scope(self):
    #     self.assertEqual(self._scope.get_scopes()[1].get_name(), "je_sick_us_mexcio")
    # def test_2_scope_deep(self):
    #     self.assertEqual(self._scope.get_scopes()[0].get_scopes()[0].get_name(), "immediate")
    #     self.assertEqual(len(self._scope.get_scopes()[0].get_scopes()[0].get_statements()),0)
    # def test_3_scope_deep(self):
    #     self.assertEqual(self._scope.get_scopes()[0].get_scopes()[0].get_scopes()[0].get_name(), "set_variable")
    #     self.assertEqual(len(self._scope.get_scopes()[0].get_scopes()[0].get_scopes()[0].get_statements()),2)
    # def test_empty_scope(self):
    #     self.assertEqual(self._scope.get_scopes()[0].get_scopes()[1].get_name(), "possible")
    #     self.assertEqual(len(self._scope.get_scopes()[0].get_scopes()[1].get_statements()),0)
