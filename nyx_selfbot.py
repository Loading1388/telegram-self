from telethon import TelegramClient, events, types
from telethon.tl.functions.account import UpdateProfileRequest
import asyncio
from datetime import datetime
import random

# ---------------- CONFIG ---------------- #
api_id = 24098304        # Get from https://my.telegram.org
api_hash = 'f99d1945d37eeebbae901e3a702db708'  # Get from https://my.telegram.org
client = TelegramClient('nyx_session', api_id, api_hash)
static_name = "D:"
time_update_interval = 60  # seconds
# ---------------------------------------- #

# ---------------- UTILS ----------------- #
async def update_name():
    while True:
        current_time = datetime.now().strftime("%H:%M")
        new_name = f"{static_name} | {current_time}"
        await client(UpdateProfileRequest(first_name=new_name))
        await asyncio.sleep(time_update_interval)

# ---------------- COMMANDS --------------- #
@client.on(events.NewMessage(pattern='/ping'))
async def ping(event):
    await event.reply('Pong! ✅')

@client.on(events.NewMessage(pattern='/vibe'))
async def vibe(event):
    emojis = ['😎','🔥','😏','🤤','🥵','💀','💖','👀']
    await event.reply(random.choice(emojis))

@client.on(events.NewMessage(pattern='/say (.+)'))
async def say(event):
    text = event.pattern_match.group(1)
    await event.reply(text)

@client.on(events.NewMessage(pattern='/afk (.+)'))
async def afk(event):
    reason = event.pattern_match.group(1)
    await client(UpdateProfileRequest(about=f"AFK: {reason}"))
    await event.reply(f"AFK status set: {reason}")

@client.on(events.NewMessage(pattern='/id'))
async def id(event):
    await event.reply(f"Your user ID: {event.sender_id}\nChat ID: {event.chat_id}")

@client.on(events.NewMessage(pattern='/hack (.+)'))
async def hack(event):
    user = event.pattern_match.group(1)
    msg = await event.reply(f"Hacking {user}...\n[░░░░░░░░░░] 0%")
    for i in range(10, 101, 10):
        await asyncio.sleep(0.5)
        await msg.edit(f"Hacking {user}...\n[{'█'*i}{'░'*(10-i//10)}] {i}%")
    await msg.edit(f"Hacking {user} completed! 💀")

@client.on(events.NewMessage(pattern='/love (.+)'))
async def love(event):
    user = event.pattern_match.group(1)
    lines = [
        f"{user}, you must be a magician, 'cause every time I look at you, everyone else disappears 😏",
        f"{user}, are you a Wi-Fi signal? Because I feel a strong connection 💖",
        f"{user}, are you made of copper and tellurium? 'Cause you’re Cu-Te 😈"
    ]
    await event.reply(random.choice(lines))

@client.on(events.NewMessage(pattern='/nuke'))
async def nuke(event):
    async for msg in client.iter_messages(event.chat_id, limit=10):
        if msg.out:
            await msg.delete()
    await event.reply("Last 10 messages nuked! 💥")

bad_words = ["ننه جنده" ,"کیرم تو کص ننت" ,"حروم زاده", "گوه نخور" ]

@client.on(events.NewMessage)
async def check_bad_words(event):
    message_text = event.raw_text
    sender = await event.get_sender()

    if any(word in message_text for word in bad_words):

      await client.edit_permissions(sender.id, view_messages=False)
      await event.reply("FUCK YOU")

#-------online status check---------- #
last_check = 0
cached_status = False

async def is_session_online():
    me = await client.get_me()
    return isinstance(me.status,
types.UserStatusOnline)

async def get_online_status():
    global last_check, cached_status
    now = asyncio.get_event_loop().time()
    if now - last_check > 10:
        cached_status = await is_session_online()
        last_check = now
    return cached_status


@client.on(events.NewMessage)
async def auto_reply_private(event):
    if event.is_private:
        session_online = await get_online_status()
        if not session_online:
            await event.reply("HAMID IS OFFLINE")

# ------------- START BOT ---------------- #
async def main():
    await client.start()
    print("NYX Self-bot is online! 😈")
    await asyncio.gather(update_name(), client.run_until_disconnected())

asyncio.run(main())
