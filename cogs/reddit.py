import discord
from discord.ext import commands
from random import choice
import asyncpraw as praw


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id="WQ7ZJnaPUYrokkNdpJoT7g",
                                  client_secret="7fcIyBq8o2iXZ4Yb8JRaBDgjc2g9cw",
                                  user_agent="script:randomposts:v1.0 (by u/OddProgrammerInC)")
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online")
        
        
    @commands.command()
    async def rserb(self, ctx: commands.Context):
        
        subreddit = await self.reddit.subreddit("serbia")
        posts = []
        valid_extensions = [".jpg", ".png", ".jpeg", ".gif", ".mp4", ".mov"]
        
        async for post in subreddit.hot(limit=40):
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
            post_embed.set_footer(text=f"Objavio: {author_name}")
            await ctx.send(embed=post_embed)     
        else:
            await ctx.send("Nema postova")
    
    @commands.command()
    async def raserb(self, ctx: commands.Context):
        subreddit = await self.reddit.subreddit("AskSerbia")
        posts = []
        valid_extensions = [".jpg", ".png", ".jpeg", ".gif", ".mp4", ".mov"]
        
        async for post in subreddit.hot(limit=40):
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
            text_embed.set_footer(text=f"Objavio: {author_name}")
            await ctx.send(embed=text_embed)
        else:
            await ctx.send("Nema postova")
            
    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())
        
        
async def setup(bot):
    await bot.add_cog(Reddit(bot))
    
   
        
        