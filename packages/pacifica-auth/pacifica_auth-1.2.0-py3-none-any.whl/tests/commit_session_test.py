#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the auth session decorator."""
from unittest.mock import patch
from unittest import TestCase
from pacifica.auth.application import session_commit


class SessionCommitTest(TestCase):
    """Test the session_commit method."""

    @patch('pacifica.auth.application.cherrypy')
    def test_happy(self, cherrypy):
        """Test the happy path."""
        # pylint: disable=too-few-public-methods
        class PatchSession:
            """Fake user session object."""

            called_save = False

            def save(self):
                """Save the user session fakeit."""
                self.called_save = True

        patch_session = PatchSession()
        setattr(cherrypy, 'session', patch_session)
        session_commit()
        self.assertTrue(patch_session.called_save, 'Session commit from cherrypy must be called.')
