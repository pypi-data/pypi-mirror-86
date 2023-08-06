from django.test import TestCase
from . import *
from kepi.trilby_api.tests import create_local_person, create_local_status
import logging
import json

logger = logging.getLogger(name='kepi')

ALICE_SUMMARY = 'Remember Alice? It\'s a song about Alice.'
ALICE_SUMMARY_HTML = f'<p>{ALICE_SUMMARY}</p>'

def _response_to_dict(response):

    result = json.loads(response.content.decode('utf-8'))

    # @context is often huge, and is irrelevant for testing here
    if '@context' in result:
        del result['@context']

    logger.info('Response: %s', result)

    return result

class Tests(TestCase):

    def setUp(self):
        settings.KEPI['LOCAL_OBJECT_HOSTNAME'] = 'testserver'
        self.maxDiff = None

    def test_single_bowler_pub_view(self):

        alice = create_local_person('alice',
                note = ALICE_SUMMARY,
                )

        c = BowlerClient()
        response = c.get('/users/alice')
        self.assertEqual(response.status_code, 200)
        result = _response_to_dict(response)

        self.assertDictContainsSubset(
                {
                    'name': 'alice',
                    'id': 'https://testserver/users/alice',
                    'type': 'Person',

                    'attachment': [],
                    'endpoints': {
                        'sharedInbox': 'https://testserver/sharedInbox',
                        },
                    'featured': 'https://testserver/users/alice/featured',
                    'followers': 'https://testserver/users/alice/followers',
                    'following': 'https://testserver/users/alice/following',
                    'icon': {
                        'mediaType': 'image/jpeg',
                        'type': 'Image',
                        'url': 'https://testserver/static/defaults/avatar_1.jpg',
                        },
                    'id': 'https://testserver/users/alice',
                    'image': {
                        'mediaType': 'image/jpeg',
                        'type': 'Image',
                        'url': 'https://testserver/static/defaults/header.jpg'
                        },
                    'inbox': 'https://testserver/users/alice/inbox',
                    'manuallyApprovesFollowers': True,
                    'name': 'alice',
                    'outbox': 'https://testserver/users/alice/outbox',
                    'preferredUsername': 'alice',
                    'publicKey': {'id': 'https://testserver/users/alice#main-key',
                        'owner': 'https://testserver/users/alice',
                        'publicKey': '-----BEGIN PUBLIC KEY-----\n'
                        'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDIUCqW/lyJ9eWkqvE7wpmHacu9\n'
                        'XOOSWZsx/+B2MM/xQYpUUIMZ3cyI3yMSOa3MS14wMBWdxlWNIMF7gVKHO6L9Ppns\n'
                        'BfTLbe/QMcssQ5rHv9oAMy/hWHGyaES3vbxzqT2qMxI5bIJRpOJfDlTpAY5AVqrn\n'
                        '8sYx/1XA9YJOKFkQIQIDAQAB\n'
                        '-----END PUBLIC KEY-----'},
                    'summary': ALICE_SUMMARY_HTML,
                    'tag': [],
                    'type': 'Person',
                    'url': 'https://testserver/users/alice',
                    },
                result,
                )

    def test_featured(self):

        alice = create_local_person('alice')
        status = create_local_status(
                content = 'Hello world',
                posted_by = alice,
                )

        c = BowlerClient()
        response = c.get('/users/alice/featured')
        self.assertEqual(response.status_code, 200)
        result = _response_to_dict(response)

        self.assertDictContainsSubset(
            {
                'id': 'http://testserver/users/alice/featured',
                'totalItems': 0,
                'type': 'OrderedCollection',
                },
            result,
            )

        alice.featured = status
        alice.save()

        response = c.get('/users/alice/featured')
        self.assertEqual(response.status_code, 200)
        result = _response_to_dict(response)

        self.assertDictContainsSubset(
            {
                'id': 'http://testserver/users/alice/featured',
                'totalItems': 1,
                'type': 'OrderedCollection',
                },
            result,
            )

class TestTombstone(TestCase):

    def setUp(self):
        settings.KEPI['LOCAL_OBJECT_HOSTNAME'] = 'testserver'
        self.maxDiff = None

    def test_tombstone(self):

        queen_anne = create_local_person('queen_anne')

        c = BowlerClient()
        response = c.get('/users/queen_anne')

        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset(
                {
                    'name': 'queen_anne',
                    'id': 'https://testserver/users/queen_anne',
                    'type': 'Person',
                    },
                _response_to_dict(response),
                )

        queen_anne.gone = True
        queen_anne.save()

        response = c.get('/users/queen_anne')

        self.assertEqual(response.status_code, 410)
        self.assertDictContainsSubset(
                {
                    'id': 'https://testserver/users/queen_anne',
                    'type': 'Tombstone',
                    'former_type': 'Person',
                    },
                _response_to_dict(response),
                )
