import discord
from discord.ext import commands, tasks
import os
import asyncio
from itertools import cycle

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

bot_statuses = cycle(["Burning King's Landing"])
                    
@tasks.loop(seconds=50)

async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))

@bot.event
async def on_ready():
    print("bot ready")
    change_bot_status.start()
    
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







