#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the auth session decorator."""
from argparse import ArgumentParser
from unittest import TestCase
from pacifica.auth.application import create_argparser


class CreateArgparserTest(TestCase):
    """Test the create_argparser method."""

    def test_happy(self):
        """Test the happy path."""
        def parser_callback(parser):
            self.assertEqual(type(parser), ArgumentParser, 'parser in callback must be ArgumentParser')
        parser = create_argparser('Some description', parser_callback=parser_callback)
        self.assertEqual(type(parser), ArgumentParser, 'Return type should also be ArgumentParser')
