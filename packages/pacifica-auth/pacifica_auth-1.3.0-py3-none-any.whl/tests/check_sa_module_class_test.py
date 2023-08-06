#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the auth session decorator."""
from unittest import TestCase
from pacifica.auth.application import check_sa_module_class


class SAModuleClassTest(TestCase):
    """Test the check_sa_module_class method."""

    def test_happy(self):
        """Test the happy path."""
        self.assertEqual(
            check_sa_module_class('social_core.backends', 'github', 'GithubOAuth2'),
            None,
            'Happy path must not return anything'
        )

    def test_module_error(self):
        """Test a bad module name."""
        with self.assertRaises(ValueError):
            check_sa_module_class('social_core.backends', 'module_not_there', 'blah')
        with self.assertRaises(ValueError):
            check_sa_module_class('social_core.backends', 'github', 'class_not_there')
