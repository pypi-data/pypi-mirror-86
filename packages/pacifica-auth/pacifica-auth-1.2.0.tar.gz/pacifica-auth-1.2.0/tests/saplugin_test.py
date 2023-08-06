#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the auth session decorator."""
from unittest.mock import patch
from unittest import TestCase
import cherrypy
from pacifica.auth.saplugin import SAEnginePlugin


class MockSession:
    """Mock session class for testing."""

    rollback_called = False
    remove_called = False

    # pylint: disable=no-self-use
    def commit(self):
        """Commit the session fakeit."""
        raise RuntimeError('Something failed')

    def rollback(self):
        """Rollback the session fakeit."""
        self.rollback_called = True

    def remove(self):
        """Remove the session fakeit."""
        self.remove_called = True


class SAPluginTest(TestCase):
    """Test the create_argparser method."""

    @patch('pacifica.auth.saplugin.scoped_session', return_value=MockSession())
    def test_commit_error(self, scopedsession_mock):
        """Test the happy path."""
        saplugin = SAEnginePlugin(cherrypy.engine, 'somedburl')
        self.assertTrue(scopedsession_mock.called, 'Scoped session must be called')
        self.assertEqual(type(saplugin.session), MockSession, 'Must override internal session with mock object.')
        with self.assertRaises(Exception):
            saplugin.commit()
        # pylint: disable=no-member
        self.assertTrue(saplugin.session.rollback_called, 'Rollback must be called')
        self.assertTrue(saplugin.session.remove_called, 'Remove must be called')
