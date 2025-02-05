import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bot token from the environment variables
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Check if the token is found
if TOKEN is None:
    raise ValueError("No token found. Please set the DISCORD_BOT_TOKEN environment variable.")

# Define bot intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent for commands

# Initialize the bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot is Ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Command: Ping
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# Run the bot
bot.run(TOKEN)


