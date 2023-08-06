from rest_framework.test import APIClient, force_authenticate
from kepi.trilby_api.views import *
from kepi.trilby_api.tests import *
from kepi.trilby_api.models import *
from django.conf import settings

# Tests for methods for the instance as a whole. API docs are here:
# https://docs.joinmastodon.org/methods/instance/

class TestInstance(TrilbyTestCase):

    def test_instance_query(self):

        content = self.get(
                '/api/v1/instance',
                )
        for k in [
                "uri", "title", "description",
                "email", "version",
                "urls", "languages", "contact_account",
                ]:
            self.assertIn(k, content)

    def test_get_emojis(self):

        content = self.get(
                '/api/v1/custom_emojis',
                )

        self.assertEqual(
                content,
                [],
                )
