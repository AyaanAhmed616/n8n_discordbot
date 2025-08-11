import os
import discord
import aiohttp

# ==== SETTINGS ====
WEBHOOK_URL = "https://ayaanahmed.app.n8n.cloud/webhook/0321da48-aa3b-4010-854d-57c5cfc1bdd1" 
GENERAL_CHANNEL_ID = 1402541828712042633  # Your General channel ID

# Get bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN') or os.getenv('TOKEN') or os.getenv('DISCORD_TOKEN')

if not BOT_TOKEN:
    print("Error: Bot token not found in environment variables!")
    print("Please set BOT_TOKEN, TOKEN, or DISCORD_TOKEN in your environment.")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    print(f'Monitoring channel ID: {GENERAL_CHANNEL_ID}')
    print('Listening for messages containing "hakla"...')

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Only process messages from General channel that include "hakla"
    if message.channel.id == GENERAL_CHANNEL_ID and "hakla" in message.content.lower():
        print(f"Hakla detected from {message.author}: {message.content}")
        
        payload = {
            "author": str(message.author),
            "content": message.content
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(WEBHOOK_URL, json=payload) as response:
                    if response.status == 200:
                        print("✅ Webhook sent successfully!")
                    else:
                        print(f"⚠️ Webhook failed with status: {response.status}")
        except Exception as e:
            print(f"❌ Error sending webhook: {e}")

print("Starting Discord bot...")
bot.run(BOT_TOKEN)
