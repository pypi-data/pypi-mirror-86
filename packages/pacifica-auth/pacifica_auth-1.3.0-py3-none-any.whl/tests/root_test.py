#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the auth session decorator."""
from os.path import join
from unittest.mock import patch
from unittest import TestCase
from cherrypy import HTTPRedirect
from pacifica.auth.root import Root


class RootUnitTest(TestCase):
    """Test the Root method."""

    @patch('cherrypy.request')
    def test_index_redirect(self, cp_request):
        """Test the happy path."""
        setattr(cp_request, 'user', 'Something True')
        with self.assertRaises(HTTPRedirect):
            Root('github', 'some_app_dir').index()

    @patch('pacifica.auth.root.serve_file')
    def test_app_args(self, cp_serve_file):
        """Test the app method with args."""
        Root('github', 'some_app_dir').app()
        self.assertTrue(cp_serve_file.called, 'serve_file should be called.')
        self.assertEqual(cp_serve_file.call_args, ((join('some_app_dir', 'index.html'),),),
                         'arguments should be the index.html for app_dir.')
        Root('github', 'some_app_dir').app('manifest.json')
        self.assertTrue(cp_serve_file.called, 'serve_file should be called.')
        self.assertEqual(cp_serve_file.call_args, ((join('some_app_dir', 'manifest.json'),),),
                         'arguments should be the manifest.json in app_dir.')

    def test_app_args_redirect(self):
        """Check the app without user info."""
        with self.assertRaises(HTTPRedirect):
            Root('github', 'some_app_dir').app('some', 'file', 'path')

    def test_done(self):
        """Check done without user info."""
        with self.assertRaises(HTTPRedirect):
            Root('github', 'some_app_dir').done()

    def test_logout(self):
        """Check logout without user info."""
        with self.assertRaises(HTTPRedirect):
            Root('github', 'some_app_dir').logout()

    @patch('pacifica.auth.root.cherrypy')
    def test_logout_with_session(self, cherrypy):
        """Test logout with user info."""
        # pylint: disable=too-few-public-methods
        class PatchSession:
            """Fake session object."""

            called_clear = False

            def clear(self):
                """Clear the user session fakeit."""
                self.called_clear = True
        patch_session = PatchSession()
        setattr(cherrypy, 'session', patch_session)
        setattr(cherrypy, 'HTTPRedirect', HTTPRedirect)
        with self.assertRaises(HTTPRedirect):
            Root('github', 'some_app_dir').logout()
        self.assertTrue(patch_session.called_clear, 'with valid user session clear must be called.')
