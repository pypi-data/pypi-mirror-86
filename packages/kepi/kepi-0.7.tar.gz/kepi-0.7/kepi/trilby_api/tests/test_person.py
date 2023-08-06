# test_person.py
#
# Part of kepi.
# Copyright (c) 2018-2020 Marnanel Thurman.
# Licensed under the GNU Public License v2.

from kepi.trilby_api.tests import *
from kepi.bowler_pub.tests import create_remote_person, mock_remote_object
from rest_framework.test import APIClient, force_authenticate
import logging
import httpretty

logger = logging.getLogger(name='kepi')

REMOTE_FOLLOWERS_COLLECTION = """{
"@context":"https://www.w3.org/ns/activitystreams",
"id":"https://example.com/users/peter/followers",
"type":"OrderedCollection",
"totalItems":3,
"orderedItems": [
"https://example.com/users/quentin",
"https://example.com/users/roger",
"https://testserver/users/alice",
"https://testserver/users/bob"
]}"""

# This needs expanding into a full unit test.

class TestPerson(TrilbyTestCase):

    @httpretty.activate
    def test_followers(self):

        alice = create_local_person(name='alice',
                auto_follow=False)
        bob = create_local_person(name='bob',
                auto_follow=False)
        carol = create_local_person(name='carol',
                auto_follow=False)

        peter = create_remote_person(
                remote_url = "https://example.com/users/peter",
                name = "peter",
                auto_fetch = True,
                )
        quentin = create_remote_person(
                remote_url = "https://example.com/users/quentin",
                name = "quentin",
                auto_fetch = True,
                )
        roger = create_remote_person(
                remote_url = "https://example.com/users/roger",
                name = "roger",
                auto_fetch = True,
                )

        Follow(follower=bob, following=alice).save()
        Follow(follower=carol, following=alice).save()
        Follow(follower=peter, following=alice).save()

        followers = sorted(list(
            [x.url for x in alice.followers]))

        self.assertEqual(
                followers,
                [
                    'https://example.com/users/peter',
                    'https://testserver/users/bob',
                    'https://testserver/users/carol',
                    ],
                )

        mock_remote_object(
                remote_url="https://example.com/users/peter/followers",
                content=REMOTE_FOLLOWERS_COLLECTION,
                )

        followers = sorted(list(
            [x.url for x in peter.followers]))

        self.assertEqual(
                followers,
                [
                    'https://example.com/users/quentin',
                    'https://example.com/users/roger',
                    'https://testserver/users/alice',
                    'https://testserver/users/bob',
                    ],
                )

    def test_has_liked(self):
        alice = create_local_person(name='alice',
                auto_follow=False)
        bob = create_local_person(name='bob',
                auto_follow=False)

        status1 = create_local_status(
                content = 'A crowd flowed over London Bridge, so many',
                posted_by = bob,
                )
        status2 = create_local_status(
                content = 'I had not thought that death had undone so many',
                posted_by = bob,
                )

        Like(liker=alice, liked=status1).save()

        self.assertTrue(
                alice.has_liked(status1),
                )
        self.assertFalse(
                alice.has_liked(status2),
                )
