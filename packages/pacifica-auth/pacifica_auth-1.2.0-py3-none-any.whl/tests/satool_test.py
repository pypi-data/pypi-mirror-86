#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the auth session decorator."""
from unittest import TestCase
from pacifica.auth.satool import SATool


class SAToolTest(TestCase):
    """Test the create_argparser method."""

    def test_commit_error(self):
        """Test the happy path."""
        satool = SATool()
        self.assertEqual(satool.commit_transaction(), None, 'Must return if db is not initialized.')
