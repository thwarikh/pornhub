from telethon import events
from datetime import datetime


@borg.on(events.NewMessage(pattern=r"\.porn", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("🔞Sux Plz🔞")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit("🔞Sux Plz🔞\n{}".format(ms))
