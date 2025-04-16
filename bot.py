import os

import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("JoinRequestBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

logging.basicConfig(level=logging.INFO)

@app.on_message(filters.command("run") & filters.group)
async def approve_all(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Only allow admins to run the command
    member = await app.get_chat_member(chat_id, user_id)
    if member.status not in ["administrator", "creator"]:
        return await message.reply("❌ Only admins can run this command.")

    approved = 0
    while True:
        try:
            async for req in app.get_chat_join_requests(chat_id):
                await app.approve_chat_join_request(chat_id, req.from_user.id)
                approved += 1
                await asyncio.sleep(0.3)
            break
        except FloodWait as e:
            logging.warning(f"Sleeping {e.value}s due to FloodWait")
            await asyncio.sleep(e.value)
        except Exception as e:
            logging.error(str(e))
            break

    await message.reply(f"✅ Approved {approved} join requests!")

app.run()
