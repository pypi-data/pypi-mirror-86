from django.conf import settings
from django.test import TestCase, Client
from kepi.trilby_api.tests import create_local_person
import kepi.trilby_api.utils as trilby_utils
import kepi.trilby_api.models as trilby_models
import httpretty
import logging
import json

ALICE_ID = 'https://altair.example.com/users/alice'
OUTBOX = ALICE_ID+'/outbox'
OUTBOX_PATH = '/users/alice/outbox'

MIME_TYPE = 'application/activity+json'

logger = logging.getLogger(name='kepi')

class Tests(TestCase):

    def setUp(self):
        settings.KEPI['LOCAL_OBJECT_HOSTNAME'] = 'testserver'
        settings.ALLOWED_HOSTS = [
                'altair.example.com',
                'testserver',
                ]

        keys = json.load(open('kepi/bowler_pub/tests/keys/keys-0001.json', 'r'))

        self._alice = create_local_person(
                name='alice',
                publicKey=keys['public'],
                privateKey=keys['private'],
                )

        super().setUp()

    # XXX Add a boolean flag about whether to authenticate self
    def _get(self,
            url,
            client):

        response = client.get(url,
                HTTP_ACCEPT = MIME_TYPE,
                )

        self.assertEqual(
                response.status_code,
                200)

        return json.loads(
                str(response.content, encoding='UTF-8'))

    # XXX Add a boolean flag about whether to authenticate self
    def _get_collection(self, url,
            client=None):

        logger.debug('------------------')
        logger.debug('Get collection: %s', url)
        if not client:
            client = Client()

        result = []
        linkname = 'first'

        while True:
            logger.debug('  -- get page: %s', url)
            page = self._get(url, client)
            logger.debug('    -- received %s', url)

            if 'orderedItems' in page:
                result.extend(page['orderedItems'])

            if linkname not in page:
                logger.info('  -- done; collection contains: %s',
                        result)
                return result

            url = page[linkname]
            linkname = 'next'

    def _add_Victoria_Wood_post(self):
        result = trilby_models.Status(
                account = self._alice,
                visibility = trilby_utils.VISIBILITY_PUBLIC,
                content = "<p>Victoria Wood parodying Peter Skellern. I laughed so much at this, though you might have to know both singers&apos; work in order to find it quite as funny.</p><p>- love song<br />- self-doubt<br />- refs to northern England<br />- preamble<br />- piano solo<br />- brass band<br />- choir backing<br />- love is cosy<br />- heavy rhotic vowels</p><p><a href=\"https://youtu.be/782hqdmnq7g\" rel=\"nofollow noopener\" target=\"_blank\"><span class=\"invisible\">https://</span><span class=\"\">youtu.be/782hqdmnq7g</span><span class=\"invisible\"></span></a></p>",
                 )

        result.save()
        return result

    def test_read_empty(self):

        contents = self._get_collection(OUTBOX)

        self.assertEqual(
                len(contents),
                0)

    def test_read_create(self):

        self._add_Victoria_Wood_post()
        contents = self._get_collection(OUTBOX)

        self.assertEqual(
                [x['type'] for x in contents],
                ['Create'])

    def test_read_announce(self):

        victoria_wood = self._add_Victoria_Wood_post()

        boost = trilby_models.Status(
                account = self._alice,
                reblog_of = victoria_wood,
                 )
        boost.save()

        contents = self._get_collection(OUTBOX)

        self.assertEqual(
                [x['type'] for x in contents],
                ['Create', 'Announce'])

    def test_following_and_followers(self):

        bob = create_local_person('bob')
        charlie = create_local_person('charlie')

        trilby_models.Follow(follower=self._alice, following=bob).save()

        self.assertEqual(
            sorted(self._get_collection(
                url = '/users/alice/following',
                )),
            [bob.url],
            )

        self.assertEqual(
            sorted(self._get_collection(
                url = '/users/alice/followers',
                )),
            [],
            )

        trilby_models.Follow(follower=self._alice, following=charlie).save()
        trilby_models.Follow(follower=charlie, following=self._alice).save()

        self.assertEqual(
            sorted(self._get_collection(
                url = '/users/alice/following',
                )),
            [bob.url, charlie.url],
            )

        self.assertEqual(
            sorted(self._get_collection(
                url = '/users/alice/followers',
                )),
            [charlie.url],
            )
