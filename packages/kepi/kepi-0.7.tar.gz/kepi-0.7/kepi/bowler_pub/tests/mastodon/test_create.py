# test_create.py
#
# Part of kepi.
# Copyright (c) 2018-2020 Marnanel Thurman.
# Licensed under the GNU Public License v2.

import logging
logger = logging.getLogger(name="kepi")

from django.test import TestCase
from unittest import skip, expectedFailure
import httpretty
from kepi.trilby_api.tests import create_local_status, create_local_person
from django.conf import settings
from kepi.bowler_pub.create import create
import kepi.bowler_pub.tests as bowler_tests
import kepi.trilby_api.utils as trilby_utils
import kepi.trilby_api.models as trilby_models
from kepi.sombrero_sendpub.fetch import fetch

REMOTE_ALICE = 'https://somewhere.example.com/users/alice'
LOCAL_FRED = 'https://testserver/users/fred'
LOCAL_STATUS_ID = 'https://testserver/status/this-is-an-id'

class Create_TestCase(TestCase):

    @httpretty.activate
    def setUp(self):
        settings.KEPI['LOCAL_OBJECT_HOSTNAME'] = 'testserver'
        self._fred = create_local_person(
                name = 'fred',
                )
        self._remote_alice = bowler_tests.create_remote_person(
            remote_url = REMOTE_ALICE,
            name = 'alice',
            auto_fetch = True,
            )

class Tests(Create_TestCase):
    def _send_create_for_object(self,
            object_form,
            sender = None,
            ):

        if sender is None:
            sender = self._fred.url
        elif not isinstance(sender, str):
            sender = sender.url

        create_form = {
                'id': LOCAL_STATUS_ID,
                '@context': 'https://www.w3.org/ns/activitystreams',
                'type': 'Create',
                'actor': sender,
                'object': object_form,
        }

        logger.info('Submitting Create activity: %s', create_form)

        create(create_form)

        if 'content' in object_form:
            return self._status_with_content(object_form['content'])
        else:
            return None

    def _status_with_content(self, content):

        import kepi.trilby_api.models as trilby_models

        result = trilby_models.Status.objects.filter(
                content = content,
                )

        if result:
            return result[0]
        else:
            return None

    def test_unknown_object_type(self):
        object_form = {
            'type': 'Banana',
            'content': 'Lorem ipsum',
          }

        status = self._send_create_for_object(object_form)

        self.assertIsNone(
                status,
                msg = 'it does not create a status',
                )

    @httpretty.activate
    def test_standalone(self):
        object_form = {
            'id': 'https://example.com/status/987',
            'attributedTo': REMOTE_ALICE,
            'type': 'Note',
            'content': 'Lorem ipsum',
          }

        status = self._send_create_for_object(object_form)

        self.assertIsNotNone(
                status,
                msg = 'it creates status',
                )

        self.assertEqual(
                status.text,
                'Lorem ipsum',
                msg = 'it creates status text',
                )

        self.assertEqual(
                status.visibility,
                trilby_utils.VISIBILITY_DIRECT,
                msg = 'missing to/cc defaults to direct privacy',
                )

    @httpretty.activate
    def test_public(self):
        object_form = {
            'id': 'https://example.com/status/987',
            'attributedTo': REMOTE_ALICE,
            'type': 'Note',
            'content': 'Lorem ipsum',
            'to': 'https://www.w3.org/ns/activitystreams#Public',
          }

        status = self._send_create_for_object(object_form)

        self.assertIsNotNone(
                status,
                msg = 'it creates status',
                )

        self.assertEqual(
                status.text,
                'Lorem ipsum',
                msg = 'it creates status text',
                )

        self.assertEqual(
                status.visibility,
                trilby_utils.VISIBILITY_PUBLIC,
                msg = 'status is public',
                )

    @httpretty.activate
    def test_unlisted(self):
        object_form = {
            'id': 'https://example.com/status/555',
            'attributedTo': REMOTE_ALICE,
            'type': 'Note',
            'content': 'Lorem ipsum',
            'cc': 'https://www.w3.org/ns/activitystreams#Public',
          }

        status = self._send_create_for_object(object_form)

        self.assertIsNotNone(
                status,
                msg = 'it creates status',
                )

        self.assertEqual(
                status.text,
                'Lorem ipsum',
                msg = 'it creates status text',
                )

        self.assertEqual(
                status.visibility,
                trilby_utils.VISIBILITY_UNLISTED,
                msg = 'status is unlisted',
                )

    @skip("""
        I have no idea how we can test whether "to" is a
        followers list if it's on another server! What
        does masto do?
    """)
    @httpretty.activate
    def test_private(self):
        object_form = {
            'id': 'https://example.com/status/987',
            'attributedTo': REMOTE_ALICE,
            'type': 'Note',
            'content': 'Lorem ipsum',
            'to': 'https://testserver/users/fred/followers',
          }

        status = self._send_create_for_object(object_form)

        self.assertIsNotNone(
                status,
                msg = 'it creates status',
                )

        self.assertEqual(
                status.text,
                'Lorem ipsum',
                msg = 'it creates status text',
                )

        self.assertEqual(
                status.visibility,
                trilby_utils.VISIBILITY_PRIVATE,
                msg = 'status is private',
                )

    @skip(""""Mastodon spec requires VISIBILITY_LIMITED here
    but it doesn't define a visibility named "limited".
    I think this is an error in the spec.""")
    @httpretty.activate
    def test_limited(self):

        object_form = {
            'id': 'https://example.com/status/987',
            'attributedTo': REMOTE_ALICE,
            'type': 'Note',
            'content': 'Lorem ipsum',
            'to': self._fred.id,
          }

        status = self._send_create_for_object(object_form)

        self.assertIsNotNone(
                status,
                msg = 'it creates status',
                )

        self.assertEqual(
                status.visibility,
                trilby_utils.VISIBILITY_LIMITED,
                msg = 'status is limited',
                )

    @httpretty.activate
    def test_direct(self):

        object_form = {
            'id': 'https://example.com/status/456',
            'type': 'Note',
            'content': 'Lorem ipsum',
            'attributedTo': REMOTE_ALICE,
            'to': LOCAL_FRED,
            'tag': {
                'type': 'Mention',
                'href': LOCAL_FRED,
                },
          }

        status = self._send_create_for_object(object_form)

        self.assertIsNotNone(
                status,
                msg = 'it creates status',
                )

        self.assertEqual(
                status.visibility,
                trilby_utils.VISIBILITY_DIRECT,
                msg = 'status is direct',
                )

    @httpretty.activate
    def test_as_reply(self):

        original_status = create_local_status(posted_by=self._fred)

        self._remote_alice = bowler_tests.create_remote_person(
            remote_url = REMOTE_ALICE,
            name = 'alice',
            auto_fetch = True,
            )

        object_form = {
            'id': 'https://example.com/status/123',
            'type': 'Note',
            'content': 'Lorem ipsum',
            'inReplyTo': original_status.url,
            'attributedTo': REMOTE_ALICE,
          }

        status = self._send_create_for_object(object_form)

        self.assertIsNotNone(
                status,
                msg = 'it creates status',
                )

        self.assertIn(
                original_status,
                status.thread,
                msg = 'status is in the thread',
                )

        self.assertEqual(
                status.is_reply,
                True,
                msg = 'status is a reply',
                )

        self.assertEqual(
                status.in_reply_to_account_id,
                original_status.account.id,
                msg = 'status is a reply to the correct account',
                )

        self.assertEqual(
                status.conversation,
                original_status.conversation,
                msg = 'status is in the same conversation',
                )

    @httpretty.activate
    def test_with_mentions(self):

        object_form = {
            'id': 'https://example.com/status/987',
            'attributedTo': REMOTE_ALICE,
            'type': 'Note',
            'content': 'Lorem ipsum',
            'tag': [
              {
                'type': 'Mention',
                'href': self._fred.url,
              },
            ],
          }

        status = self._send_create_for_object(object_form)

        self.assertIsNotNone(
                status,
                msg = 'it creates status',
                )

        self.assertIn(
                self._fred,
                status.tags,
                msg = 'status mentions self._fred',
                )

    @httpretty.activate
    def test_with_mentions_missing_href(self):

        object_form = {
            'id': 'https://example.com/status/987',
            'attributedTo': REMOTE_ALICE,
            'type': 'Note',
            'content': 'Lorem ipsum',
            'tag': [
              {
                'type': 'Mention',
              },
            ],
          }

        status = self._send_create_for_object(object_form)

        self.assertIsNotNone(
                status,
                msg = 'it creates status',
                )

    # For the time being, ignoring tests for:
    #   - media
    #   - hashtags
    #   - emoji
    #   - polls

    @httpretty.activate
    def test_when_sender_is_followed_by_local_users(self):

        from kepi.trilby_api.models import Follow, Person

        local_user = create_local_person()
        remote_alice = fetch(REMOTE_ALICE,
                expected_type = Person)

        following = Follow(
                follower = local_user,
                following = remote_alice,
                )
        following.save()

        object_form = {
            'id': 'https://example.com/some-note',
            'type': 'Note',
            'content': 'Lorem ipsum',
          }

        status = self._send_create_for_object(object_form,
                sender=remote_alice)

        self.assertIsNotNone(
                status,
                msg = 'it creates status',
                )

        self.assertEqual(
                status.text,
                'Lorem ipsum',
                msg = 'it creates status text',
                )

    @httpretty.activate
    def test_when_sender_replies_to_local_status(self):

        local_status = create_local_status(posted_by=self._fred)

        object_form = {
            'id': 'https://example.com/status/987',
            'attributedTo': REMOTE_ALICE,
            'type': 'Note',
            'content': 'Lorem ipsum',
            'inReplyTo': local_status.url,
          }

        status = self._send_create_for_object(object_form)

        self.assertIsNotNone(
                status,
                msg = 'it creates status',
                )

        self.assertEqual(
                status.text,
                'Lorem ipsum',
                msg = 'it creates status text',
                )

    @httpretty.activate
    def test_when_sender_targets_a_local_user(self):

        local_user = create_local_person()

        object_form = {
            'id': 'https://example.com/status/987',
            'attributedTo': REMOTE_ALICE,
            'type': 'Note',
            'content': 'Lorem ipsum',
            'to': local_user.id,
          }

        status = self._send_create_for_object(object_form)

        self.assertIsNotNone(
                status,
                msg = 'it creates status',
                )

        self.assertEqual(
                status.text,
                'Lorem ipsum',
                msg = 'it creates status text',
                )

    @httpretty.activate
    def test_when_sender_ccs_a_local_user(self):

        local_user = create_local_person()

        object_form = {
            'id': 'https://example.com/status/987',
            'attributedTo': REMOTE_ALICE,
            'type': 'Note',
            'content': 'lorem ipsum',
            'cc': local_user.id,
          }

        status = self._send_create_for_object(object_form)

        self.assertIsNotNone(
                status,
                msg = 'it creates status',
                )

        self.assertEqual(
                status.text,
                'lorem ipsum',
                msg = 'it creates status text',
                )

    @skip("""
    # XXX What are the terms
    # under which masto will decide that
    # a sender has no relevance to local activity?
    # Does it make a difference whether the message
    # was submitted to the shared inbox?
    # Check through masto's code.
    """)
    @httpretty.activate
    def test_when_sender_has_no_relevance_to_local_activity(self):

        local_user = create_local_person()

        object_form = {
            'id': 'https://example.com/status/987',
            'attributedTo': REMOTE_ALICE,
            'type': 'note',
            'content': 'lorem ipsum',
          }

        status = self._send_create_for_object(object_form,
                sender = REMOTE_ALICE)

        self.assertIsNone(
                status,
                msg = 'it does not create a status',
                )
