from telethon import TelegramClient, events
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
@client.on(events.NewMessage(pattern='/کیر'))
async def کیر(event):
    await event.reply('تو کونت جنده')

@client.on(events.NewMessage(pattern='/های'))
async def های(event):
    await event.reply('بنال، انگلیسی هم زر نزن')

@client.on(events.NewMessage(pattern='/بگو (.+)'))
async def بگو(event):
    text = event.pattern_match.group(1)
    await event.reply(text)

@client.on(events.NewMessage(pattern='/afk (.+)'))
async def afk(event):
    reason = event.pattern_match.group(1)
    await client(UpdateProfileRequest(about=f"AFK: {reason}"))
    await event.reply(f"AFK status set: {reason}")

@client.on(events.NewMessage(pattern='/ایدیش'))
async def ایدیش(event):
    await event.reply(f"Your user ID: {event.sender_id}\nChat ID: {event.chat_id}")

@client.on(events.NewMessage(pattern="/هک کن (.+)'))
async def هک کن(event):
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
async def check_bad_words(events):
    message_texting = event.raw_text
    sender = await event.get_sender()

if any(word in message_text for word in bad_words):

    await client.edit_permissions(sender.id, view_messages=False)
    await event.reply("FUCK YOU")

# ------------- START BOT ---------------- #
async def main():
    await client.start()
    print("NYX Self-bot is online! 😈")
    await asyncio.gather(update_name(), client.run_until_disconnected())


asyncio.run(main())

