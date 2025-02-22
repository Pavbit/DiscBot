import discord
from discord import app_commands
from discord.ext import commands
from random import choice
import asyncpraw as praw
from dotenv import load_dotenv
import os


env_file_path = r"C:\Users\Andrija\Desktop\bitno\maksbot\.env"
load_dotenv(env_file_path)


CLIENT_SECRET_REDDIT: str = os.getenv("CLIENT_SECRET_REDDIT")
CLIENT_ID_REDDIT: str = os.getenv("CLIENT_ID_REDDIT")

class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id= (CLIENT_ID_REDDIT),
                                  client_secret= (CLIENT_SECRET_REDDIT),
                                  user_agent="script:randomposts:v1.0 (by u/OddProgrammerInC)")
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} povezan")
        
        
    @app_commands.command(name="rgot", description="Random hot topics on r/gameofthrones")
    async def rgot(self, interaction: discord.Interaction): 
        
        subreddit = await self.reddit.subreddit("gameofthrones")
        posts = []
        valid_extensions = [".jpg", ".png", ".jpeg", ".gif"]
        
        async for post in subreddit.hot(limit=50):
            if post.author and post.author.name == "AutoModerator":
                continue
            if post.is_self or any(post.url.endswith(ext) for ext in valid_extensions):
                    posts.append(post)
         
        if posts:
            random_post = choice(posts)
            post_embed = discord.Embed(
                title=random_post.title,
                description=random_post.selftext or "No text",
                color=discord.Color.random())
            
            if not random_post.is_self and any(random_post.url.endswith(ext) for ext in valid_extensions):
                post_embed.set_image(url=random_post.url)
            author_name = random_post.author.name if random_post.author else "Unkown"
            post_embed.set_footer(text=f"Posted by u/{author_name} on r/{random_post.subreddit.display_name}")
            await interaction.response.send_message(embed=post_embed)     
        else:
            await interaction.response.send_message("No posts")
    
    @app_commands.command(name="rhotd", description="Random hot topics on r/HouseOfTheDragon")
    async def rhotd(self, interaction: discord.Interaction):
        subreddit = await self.reddit.subreddit("HouseOfTheDragon")
        posts = []
        valid_extensions = [".jpg", ".png", ".jpeg", ".gif"]
        
        async for post in subreddit.hot(limit=50):
            if post.author and post.author.name == "AutoModerator":
                continue
            if post.is_self or any(post.url.endswith(ext) for ext in valid_extensions):
                posts.append(post)
         
        if posts:
            random_post = choice(posts)
            text_embed = discord.Embed(
                title=random_post.title,
                description=random_post.selftext or "No text",
                color=discord.Color.random())

            if not random_post.is_self and any(random_post.url.endswith(ext) for ext in valid_extensions):
                text_embed.set_image(url=random_post.url)
            author_name = random_post.author.name if random_post.author else "Unkown"
            text_embed.set_footer(text=f"Posted by u/{author_name} on r/{random_post.subreddit.display_name}")
            await interaction.response.send_message(embed=text_embed)
        else:
            await interaction.response.send_message("No posts")
            
    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())
        
        
async def setup(bot):
    await bot.add_cog(Reddit(bot))
    
        