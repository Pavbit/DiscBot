import discord
from discord.ext import commands
import os
import asyncio

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Event: Bot is Ready
@bot.event
async def on_ready():
    print("bot ready")
    
with open ("token.txt") as file:
    token = file.read()

async def Load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
         await bot.load_extension(f"cogs.{filename[:-3]}")
        
        
async def main():
    async with bot:
        await Load()
        await bot.start(token)
        
asyncio.run(main())







