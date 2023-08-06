#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the auth session decorator."""
from unittest import TestCase
from pacifica.auth.user_model import User


class UserModelTest(TestCase):
    """Test the create_argparser method."""

    def test_is_auth(self):
        """Test the happy path."""
        user_obj = User()
        self.assertEqual(user_obj.is_authenticated(), True, 'The user is always authenticated.')
