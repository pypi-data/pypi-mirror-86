#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the auth session decorator."""
from unittest.mock import patch
from unittest import TestCase
from json import loads
from pacifica.auth import error_page_default


class ErrorPageTest(TestCase):
    """Test the error_page_default method."""

    @patch('cherrypy.response')
    def test_happy(self, cp_response):
        """Test the happy path."""
        setattr(cp_response, 'headers', {})
        ret_obj = error_page_default(some='key', words='and', stuff='blah')
        self.assertTrue('Content-Type' in cp_response.headers, 'Headers should have Content-Type set.')
        self.assertEqual(cp_response.headers.get('Content-Type'),
                         'application/json', 'Content type must be application/json')
        self.assertEqual(type(ret_obj), bytes, 'Return object should be of type bytes')
        json_obj = loads(ret_obj)
        self.assertEqual(json_obj.get('some'), 'key', 'kwargs passed should come out as a dictionary')
        self.assertEqual(json_obj.get('words'), 'and', 'kwargs passed should come out as a dictionary')
        self.assertEqual(json_obj.get('stuff'), 'blah', 'kwargs passed should come out as a dictionary')
