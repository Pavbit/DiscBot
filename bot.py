import discord
from discord.ext import commands, tasks
import os
import asyncio
from itertools import cycle
from dotenv import load_dotenv

env_file_path = r"C:\Users\Andrija\Desktop\bitno\maksbot\.env"
load_dotenv(env_file_path)


TOKEN: str = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())



bot_statuses = cycle(["Burning King's Landing", "Flying over Westeros", "Resting at Valyria"])

                    
@tasks.loop(seconds=300)

async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))

@bot.event
async def on_ready():
    print("bot radi")
    change_bot_status.start()
    try:
        synced_commands = await bot.tree.sync()
        print(f"Ucitano {len(synced_commands)} komandi.")
    except Exception as e:
        print("Greska pri sinhronizaciji komandi", e)
        
#@bot.tree.command(name="test", description="test")
#async def testi(interaction: discord.Interaction):
    #await interaction.response.send_message(f"poz {interaction.user.mention}")



async def Load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
         await bot.load_extension(f"cogs.{filename[:-3]}")
        
        
async def main():
    async with bot:
        await Load()
        await bot.start(TOKEN)
        
asyncio.run(main())







