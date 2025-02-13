import discord
from discord import app_commands
from discord.ext import commands
from random import choice
import asyncpraw as praw
from dotenv import load_dotenv
import os

env_file_path = r"C:\Users\Andrija\Desktop\bitno\maksbot\.env"
load_dotenv(env_file_path)


REDDIT_API: str = os.getenv("REDDIT_API")
CLIENT_ID_REDDIT: str = os.getenv("CLIENT_ID_REDDIT")

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id= (CLIENT_ID_REDDIT),
                                  client_secret= (REDDIT_API),
                                  user_agent="script:randomposts:v1.0 (by u/OddProgrammerInC)")
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} povezan")
        
        
    @app_commands.command(name="rserb", description="Random hot postovi sa r/serbia.")
    async def rserb(self, interaction: discord.Interaction): 
        
        subreddit = await self.reddit.subreddit("serbia")
        posts = []
        valid_extensions = [".jpg", ".png", ".jpeg", ".gif"]
        
        async for post in subreddit.hot(limit=100):
            if post.author and post.author.name == "AutoModerator":
                continue
            if post.is_self or any(post.url.endswith(ext) for ext in valid_extensions):
                    posts.append(post)
         
        if posts:
            random_post = choice(posts)
            post_embed = discord.Embed(
                title=random_post.title,
                description=random_post.selftext or "Nema teksta",
                color=discord.Color.random())
            
            if not random_post.is_self and any(random_post.url.endswith(ext) for ext in valid_extensions):
                post_embed.set_image(url=random_post.url)
            author_name = random_post.author.name if random_post.author else "Nepoznat"
            post_embed.set_footer(text=f"Objavio u/{author_name} na r/{random_post.subreddit.display_name}")
            await interaction.response.send_message(embed=post_embed)     
        else:
            await interaction.response.send_message("Nema postova")
    
    @app_commands.command(name="raserb", description="Random hot postovi sa r/AskSerbia.")
    async def raserb(self, interaction: discord.Interaction):
        subreddit = await self.reddit.subreddit("AskSerbia")
        posts = []
        valid_extensions = [".jpg", ".png", ".jpeg", ".gif"]
        
        async for post in subreddit.hot(limit=100):
            if post.author and post.author.name == "AutoModerator":
                continue
            if post.is_self or any(post.url.endswith(ext) for ext in valid_extensions):
                posts.append(post)
         
        if posts:
            random_post = choice(posts)
            text_embed = discord.Embed(
                title=random_post.title,
                description=random_post.selftext or "Nema teksta",
                color=discord.Color.random())

            if not random_post.is_self and any(random_post.url.endswith(ext) for ext in valid_extensions):
                text_embed.set_image(url=random_post.url)
            author_name = random_post.author.name if random_post.author else "Nepoznat"
            text_embed.set_footer(text=f"Objavio u/{author_name} na r/{random_post.subreddit.display_name}")
            await interaction.response.send_message(embed=text_embed)
        else:
            await interaction.response.send_message("Nema postova")
            
    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())
        
        
async def setup(bot):
    await bot.add_cog(Reddit(bot))
    
        