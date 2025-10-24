import os
import asyncio
import random
from datetime import datetime
from telethon import TelegramClient, events, types
from telethon.tl.functions.account import UpdateProfileRequest
from dotenv import load_dotenv

# ---------------- CONFIG ---------------- #
load_dotenv()  # reads .env file if exists
api_id = int(os.getenv("API_ID", "24098304"))
api_hash = os.getenv("API_HASH", "f99d1945d37eeebbae901e3a702db708")
client = TelegramClient("nyx_session", api_id, api_hash)

static_name = "D:"
time_update_interval = 30  # seconds
# ---------------------------------------- #

# Track who got the “offline” message already
offline_replied_users = set()

# ---------------- UTILS ----------------- #
async def update_name():
    """Keeps updating display name with time every 30s."""
    while True:
        try:
            current_time = datetime.now().strftime("%H:%M")
            new_name = f"{static_name} | {current_time}"
            await client(UpdateProfileRequest(first_name=new_name))
        except Exception as e:
            print(f"[update_name] Error: {e}")
        await asyncio.sleep(time_update_interval)


async def is_online():
    """Check session online status."""
    try:
        me = await client.get_me()
        return isinstance(me.status, types.UserStatusOnline)
    except Exception:
        return False

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

@client.on(events.NewMessage(pattern=r"/nuke"))
async def nuke(event):
    deleted = 0
    async for msg in client.iter_messages(event.chat_id, limit=10):
        if msg.out:
            try:
                await msg.delete()
                deleted += 1
                await asyncio.sleep(0.1)
            except Exception:
                pass
    await event.reply(f"Nuked {deleted} messages 💥")

#----------- BAD WORDS FILTER--------#

bad_words = ["ننه جنده" ,"کیرم تو کص ننت" ,"حروم زاده", "گوه نخور"]

@client.on(events.NewMessage)
async def badword_filter(event):
    if not (event.is_group or event.is_channel):
        return
    if any(bad in event.raw_text for bad in bad_words):
        try:
            await event.reply("FUCK YOU 😤")
            await asyncio.sleep(1)
            await client.edit_permissions(event.chat_id, event.sender_id, view_messages=False)
        except Exception as e:
            print(f"[badword_filter] Error: {e}")

#--------AUTO OFFLINE REPLY-------------#
@client.on(events.NewMessage)
async def auto_reply_private(event):
    if not event.is_private:
        return
    user_id = event.sender_id
    try:
        online = await is_online()
        if not online and user_id not in offline_replied_users:
            await event.reply("HAMID IS OFFLINE")
            offline_replied_users.add(user_id)
        elif online and user_id in offline_replied_users:
            # Reset when you come back online
            offline_replied_users.remove(user_id)
    except Exception as e:
        print(f"[auto_reply_private] Error: {e}")

# ------------- START BOT ---------------- #
async def main():
    await client.start()
    print("NYX Self-bot is online! 😈")
    await asyncio.gather(update_name(), client.run_until_disconnected())

asyncio.run(main())
