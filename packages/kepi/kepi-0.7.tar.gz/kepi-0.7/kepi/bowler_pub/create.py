# create.py
#
# Part of kepi.
# Copyright (c) 2018-2020 Marnanel Thurman.
# Licensed under the GNU Public License v2.

"""
This contains create(), which creates the appropriate
model instance when we've received an ActivityPub message.

create() is called by validate() when we've validated
the message.
"""

import logging
logger = logging.getLogger(name="kepi")

from urllib.parse import urlparse
import kepi.trilby_api.models as trilby_models
import kepi.trilby_api.utils as trilby_utils
import kepi.bowler_pub
import kepi.bowler_pub.utils as bowler_utils
import kepi.sombrero_sendpub.fetch as sombrero_fetch
import kepi.sombrero_sendpub.collections as sombrero_collections

def create(fields,
        address = None):

    if address is None:
        address = fields.get('id', '')

    logger.debug('%s: creating from %s',
            address, fields)

    if 'type' not in fields:
        logger.warning("%s: no type name; can't continue")
        return

    if '_' in fields['type']:
        # no types have underscores in their names, and
        # in this module we use the underscore to separate
        # activity type names from object type names

        logger.warning('%s: underscore in type name "%s"; looks dodgy',
                address,
                fields['type'],
                )
        return

    try:
        result = deserialise(fields)
        return result
    except Exception as e:
        logger.info("%s: can't deserialise: %s",
                address, repr(e))
        return None

def deserialise(fields,
        address = None,
        ):

    if address is None:
        address = fields.get('id', '')

    handler_name = 'on_%s' % (
            fields['type'].lower(),
            )

    if handler_name not in globals():
        logger.info("%s: no %s; returning dict",
                address, handler_name)
        return fields

    try:
        result = globals()[handler_name](fields, address)
        logger.info("%s: result from %s was %s",
                address, handler_name, result)
    except ValueError as ve:
        logger.info("%s: error from %s was %s; returning None",
                address, handler_name, ve)
        return None

    return result

def on_follow(fields, address):

    logger.debug('%s: on_follow %s', address, fields)

    if not bowler_utils.is_local(fields['object']):
        logger.info("%s: ignoring someone following non-local user",
                address)
        return None

    follower = sombrero_fetch.fetch(
            fields['actor'],
            expected_type = trilby_models.Person,
            )

    if follower is None:
        # shouldn't happen
        logger.warning('%s: could not find remote user %s',
                address,
                fields['actor'],
                )
        return None

    following = sombrero_fetch.fetch(
            fields['object'],
            expected_type = trilby_models.Person,
            )

    if following is None:
        logger.info('%s: there is no local user %s',
                address,
                fields['object'],
                )
        return None

    result = trilby_models.Follow(
            follower = follower,
            following = following,
            offer = fields.get('id'),
            )

    result.save(
            send_signal = True,
            )

    return result

def _visibility_from_fields(fields):

    def get_set(fields, fieldname):

        result = fields.get(fieldname, [])
        if isinstance(result, list):
            result = set(result)
        else:
            result = set([result])

        try:
            in_object = fields['object'].get(
                    fieldname, [])
            if isinstance(in_object, list):
                result.update(in_object)
            else:
                result.add(in_object)
        except TypeError:
            pass
        except KeyError:
            pass
        except AttributeError:
            pass

        return set(result)

    audience = dict([
        (fieldname, get_set(fields, fieldname))
        for fieldname in ['to', 'cc']
        ])

    for group, result in [
            ('to', trilby_utils.VISIBILITY_PUBLIC),
            ('cc', trilby_utils.VISIBILITY_UNLISTED),
            ]:
        for someone in audience[group]:
            if someone in kepi.bowler_pub.PUBLIC_IDS:
                return result

    # default
    return trilby_utils.VISIBILITY_DIRECT

def on_create(fields, address):

    logger.debug('%s: on_create %s', address, fields)

    newborn_fields = fields['object']
    # XXX Can fields['object'] validly be a URL?

    if 'type' not in newborn_fields:
        logger.info("%s: newborn object had no type",
                address)
        return None

    if 'attributedTo' not in newborn_fields:
        newborn_fields['attributedTo'] = fields['actor']

    logger.debug('%s:  -- recurse',
            address)

    return create(newborn_fields)

def on_note(fields, address):

    logger.debug("Looking up actor: %s",
            fields['attributedTo'])

    poster = sombrero_fetch.fetch(
        fields['attributedTo'],
        expected_type = trilby_models.Person,
        )

    if poster is None:
        logger.debug("  -- who does not exist")
        return None

    logger.debug("  -- who is %s", poster)

    if 'inReplyTo' in fields:
        in_reply_to = sombrero_fetch.fetch(
            fields['inReplyTo'],
            expected_type = trilby_models.Status,
            )
    else:
        in_reply_to = None

    is_sensitive = False # FIXME
    spoiler_text = '' # FIXME
    language = 'en' # FIXME

    visibility = _visibility_from_fields(
            fields)

    logger.debug('%s: creating status from %s',
        address,
        fields,
        )

    try:
        newbie = trilby_models.Status(
            remote_url = fields['id'],
            account = poster,
            in_reply_to = in_reply_to,
            content = fields['content'],
            sensitive = is_sensitive,
            spoiler_text = spoiler_text,
            visibility = visibility,
            language = language,
                )

        newbie.save()

        logger.debug('%s: created status %s',
            address,
            newbie,
            )

    except KeyError as ke:
        logger.debug('%s: missing field: %s',
            address,
            ke)
        return None

    except Exception as e:
        logger.debug('%s: failed to create status: %s',
            address,
            e)
        return None

    if 'tag' in fields:

        logger.debug('%s: adding tags', address)

        for tag in fields['tag']:

            if 'type' not in tag or 'href' not in tag:
                logger.debug('%s:  -- missing fields: %s',
                        address, tag)
                continue

            if tag['type'].lower() != 'mention':
                logger.debug('%s:  -- unknown tag type: %s',
                        address, tag)
                continue

            logger.debug('%s:   -- %s',
                    address, tag['href'])

            whom = sombrero_fetch.fetch(tag['href'],
                    expected_type = trilby_models.Person)

            if whom is None:
                logger.debug('%s:     -- not found',
                        address)
                continue

            mention = trilby_models.Mention(
                    status = newbie,
                    whom = whom,
                    )
            mention.save()

            logger.debug('%s:     -- %s',
                    address, mention)

        logger.debug('%s:   -- tags done',
                address)

    return newbie

def on_announce(fields, address):

    logger.debug('%s: on_announce %s', address, fields)

    try:
        if isinstance(fields.get('object', None), dict):
            # We don't trust an object passed to us as part of
            # an Announce, because it generally comes from a
            # different user. So we take the id and go and
            # look it up for ourselves.
            status_url = fields['object']['id']
        else:
            status_url = fields['object']
    except FieldError as fe:
        logger.info("%s: unusable object field: %s",
                address, fe)
        return None

    status = sombrero_fetch.fetch(status_url,
            expected_type = trilby_models.Status,
            )

    if status is None:

        logger.info("%s: attempted to reblog non-existent status %s",
                address, status_url)
        return None

    actor = sombrero_fetch.fetch(fields['actor'],
            expected_type = trilby_models.Person,
            )

    logger.debug('%s: reblogging status %s by %s',
            address, status_url, actor)

    reblog = trilby_models.Status(
            account = actor,
            reblog_of = status,
            )
    reblog.save()

    logger.debug('%s: created reblog: %s',
            address, reblog)

    return reblog

def on_person(fields, address,
        update_existing = False):

    if update_existing:
        try:
            user = trilby_models.RemotePerson.objects.get(
                    remote_url = fields['id'],
                    )
            logger.debug("%s: updating existing user %s",
                    address, user)
        except trilby_models.RemotePerson.DoesNotExist:
            logger.debug("%s: can't update %s because they don't exist",
                    address, fields['id'])
            return None
    else:
        user = trilby_models.RemotePerson(
                remote_url = fields['id'],
                )
        logger.debug("%s: creating new user",
                    address)

    for fieldsname, fieldname in [
            ('preferredUsername', 'username'),
            ('name', 'display_name'),
            ('summary', 'note'),
            ('manuallyApprovesFollowers', 'locked'),
            ('following', 'following_url'),
            ('followers', 'followers_url'),
            ('inbox', 'inbox_url'),
            ('outbox', 'outbox_url'),
            ('featured', 'featured_url'),
            ('created_at', 'created_at'),
            ('bot', 'bot'),
            ('movedTo', 'moved_to'),
            ]:
        if fieldsname in fields:
            logger.debug('%s:   %s = %s',
                    address, fieldname, fields[fieldsname])

            setattr(user,
                    fieldname,
                    fields[fieldsname])

    # A shared inbox takes priority over a personal inbox
    if 'endpoints' in fields:
        if 'sharedInbox' in fields['endpoints']:
            user.inbox_url = fields['endpoints']['sharedInbox']

    if 'publicKey' in fields:
        key = fields['publicKey']

        if 'owner' in key:
            if key['owner'] != user.remote_url:
                raise ValueError(
                        f"Remote user gave us someone else's key "
                                f"({key['owner']} for {user.remote_url})")

        if 'id' in key:
            user.key_name = key['id']

        if 'publicKeyPem' in key:
            user.publicKey = key['publicKeyPem']

    if user.acct is None:

        # We might already know the acct,
        # if we got to this user by looking up their acct.
        # This will probably have to be cleverer later.

        hostname = urlparse(user.remote_url).netloc
        user.acct = '{}@{}'.format(
            user.username,
            hostname,
            )

    # FIXME Header and icon

    user.save()

    return user

on_actor = on_person

def on_like(fields, address):

    logger.debug('%s: on_like %s', address, fields)

    liker = sombrero_fetch.fetch(
            fields['actor'],
            expected_type = trilby_models.Person,
            )

    if liker is None:
        # shouldn't happen
        logger.warning('%s: could not find user %s',
                address,
                fields['actor'],
                )
        return None

    liked = sombrero_fetch.fetch(
            fields['object'],
            expected_type = trilby_models.Status,
            )

    if liked is None:
        logger.info('%s: could not find status %s',
                address,
                fields['object'],
                )
        return None

    like = trilby_models.Like(
            liker = liker,
            liked = liked,
            )

    like.save(
            send_signal = True,
            )

    return like

def on_update(fields, address):

    # TODO: According to the spec, "Update" is partial
    # if we're getting the message from a local user,
    # but total if we're getting it from a remote user.
    # Since we don't currently support ActivityPub from
    # local users, we treat all updates as total for now.
    # See https://gitlab.com/marnanel/kepi/-/issues/8 .

    handler = on_person # FIXME there are other possibilities!
    # See https://gitlab.com/marnanel/kepi/-/issues/63 .

    logger.debug('%s: on_update %s', address, fields)

    changes = fields['object']

    logger.debug('%s:   -- changes: %s', address, changes)

    result = handler(changes, address,
            update_existing = True)

    return result

def on_collection(fields, address):

    result = sombrero_collections.Collection(
            remote_url = address,
            )
    result.update(fields)

    return result

on_orderedcollection = on_collection

def on_collection_page(fields, address):
    result = sombrero_collections._CollectionPage(
            remote_url = address,
            )
    result.update(fields)

    return result

on_orderedcollectionpage = on_collection_page
