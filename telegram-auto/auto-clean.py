from telethon import TelegramClient
import asyncio
from datetime import datetime, timezone

API_ID = 'enter_app_api_id_here'
API_HASH = 'enter_app_api_hash_here'
GROUP_ID = 'enter_group/channel_id_here'
SESSION_NAME = 'enter_telegram_session_name_here'

# https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.messages.MessageMethods.iter_messages
# https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.messages.MessageMethods.delete_messages


async def clean_old_message():
    delete_msg_ids = set()

    today = datetime.now(timezone.utc)

    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:

        async for message in client.iter_messages(
                entity=GROUP_ID,
                search="#notification",
                reverse=True
        ):
            print(f'ID: {message.id}, date: {message.date}, text: {message.message}')
            delete_msg_ids.add(message.id)
            if message.date > today:
                break

        print(delete_msg_ids)

        await client.delete_messages(GROUP_ID, delete_msg_ids)

if __name__ == '__main__':
    asyncio.run(clean_old_message())
