import os
from telethon import TelegramClient, events
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Retrieve API credentials and channel IDs from environment variables
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')
SOURCE_CHANNEL = os.getenv('SOURCE_CHANNEL_ID')
DESTINATION_CHANNEL = os.getenv('DESTINATION_CHANNEL_ID')
TARGET_EMOJIS = ['⚡', '❗️']  # List of target emojis

# Initialize the Telegram client
client = TelegramClient('session_name', API_ID, API_HASH)

async def main():
    # Connect to the client
    await client.start(PHONE_NUMBER)

    @client.on(events.NewMessage(chats=SOURCE_CHANNEL))
    async def handler(event):
        message = event.message
        if message.text:
            # Check if the message starts with one of the target emojis
            if any(message.text.startswith(emoji) for emoji in TARGET_EMOJIS):
                # Filter out messages containing "Реклама" or links to other Telegram channels
                if "Реклама" not in message.text and not re.search(r't\.me/\S+', message.text):
                    await client.send_message(DESTINATION_CHANNEL, message.text)

    print(f"Listening for messages in {SOURCE_CHANNEL}...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
