# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import regex

from telethon import events, utils
from telethon.tl import types, functions

nicks = storage.nicks or {}

@borg.on(events.NewMessage(pattern=r'.nick( (?P<target>\S+)|$)', outgoing=True))
@borg.on(events.NewMessage(pattern=r'.who( (?P<target>\S+)|$)', outgoing=True))
async def on_check_nick(event):
    # JSON only does string keys lololol
    target = await get_target_id(event)
    print(f"target {target}")
    if target not in nicks:
        await event.respond("no")
    else:
        await event.respond(f"nick: {nicks[target]}")

    await event.delete()

async def get_target_id(event):
    # must have the regex with target in it
    target = event.pattern_match.group("target")
    r_msg = await event.reply_message
    # if they provided an explicit target, use that over the reply user
    if target:
        if regex.match(r'[^+]-?\d+', target):
            ent = await borg.get_entity(int(target))
        else:
            ent = await borg.get_entity(target)
        target = utils.get_peer_id(ent)
        # TODO handle errors lol
    elif r_msg:
        # if its a forward do the forward dude
        # otherwise do the sender
        if r_msg.fwd_from:
            target = r_msg.fwd_from.from_id
        else:
            target = r_msg.from_id
    else:
        # didnt specify a target and didnt reply to anything
        # fuck that guy
        raise ValueError

    # JSON only does string keys lololol
    return str(target)

@borg.on(events.NewMessage(pattern=r'.nicks (?P<target>\S+ )?(?P<nick>.+)', outgoing=True))
async def on_nick_save(event):
    nick = event.pattern_match.group("nick")
    target = await get_target_id(event)
    nicks[target] = nick
    storage.nicks = nicks
    await event.delete()


@borg.on(events.NewMessage(pattern=r'.nickl', outgoing=True))
async def on_nick_list(event):
    await event.respond('set nicks: \n' + '\n'.join(
        (f'{k}: "{v}"' for k, v in nicks.items())))
    await event.delete()


@borg.on(events.NewMessage(pattern=r'.nickd( (?P<target>\S+)|$)', outgoing=True))
async def on_nick_delete(event):
    nicks.pop(await get_target_id(event), None)
    storage.nicks = nicks
    await event.delete()
