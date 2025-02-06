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
    print(f"Logged in as {bot.user}")

# Command: Test
@bot.command(name="poz", aliases=["pozdrav", "cao"]) 
async def _pozdravlja(ctx): 
    await ctx.send(f"i tebi {ctx.author.mention}")


@bot.command()
async def sendembded(ctx):
    embed = discord.Embed(title="Ime", description="Opis", color=discord.Color.random())
    embed.set_thumbnail(url=ctx.author.avatar)
    embed.add_field(name="test", value="opet", inline=False)
    embed.set_image(url=ctx.guild.icon)
    embed.set_footer(text="posle ce biti nes", icon_url=ctx.author.avatar)
    await ctx.send(embed=embed)
# Run the bot
bot.run(TOKEN)


# bot commands




