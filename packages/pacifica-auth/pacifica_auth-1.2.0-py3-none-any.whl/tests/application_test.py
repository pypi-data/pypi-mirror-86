#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the auth session decorator."""
from os.path import join, dirname
from unittest.mock import patch
from unittest import TestCase
from pacifica.auth.application import quickstart
from pacifica.auth.user_model import User


class ApplicationTest(TestCase):
    """Test the Root method."""

    @patch('pacifica.auth.application.cp_quickstart')
    def test_index_redirect(self, cp_quickstart):
        """Test the happy path."""
        quickstart(
            [], 'Basic application', User,
            'pacifica.auth.user_model.User',
            join(dirname(__file__))
        )
        self.assertTrue(cp_quickstart.called, 'CherryPy quickstart was called.')
