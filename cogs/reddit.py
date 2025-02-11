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
        
        async for post in subreddit.hot(limit=20):
            valid_extensions = [".jpg", ".png", ".jpeg", ".gif", ".mp4", ".mov"]
            if post.author is not None and any(post.url.endswith(ext) for ext in valid_extensions):
                posts.append(post)
            elif post.author is None:
                posts.append(post)
         
        if posts:
            random_post = choice(posts)
            post_embed = discord.Embed(
                title=random_post.title,
                description=random_post.selftext or "Nema teksta",
                color=discord.Color.random())
            
            #post_embed.set_author(name=f"Obavljeno od strane {ctx.author.name}", icon_url=ctx.author.avatar)
            post_embed.set_image(url=random_post.url)
            author_name = random_post.author.name if random_post.author else "Nepoznat"
            post_embed.set_footer(text=f"Objavio: {author_name}")
            await ctx.send(embed=post_embed)     
        else:
            await ctx.send("Nema postova")
    
    @commands.command()
    async def raserb(self, ctx: commands.Context):
        subreddit = await self.reddit.subreddit("AskSerbia")
        text_posts = []
        
        
        async for post in subreddit.hot(limit=20):
            if post.is_self:  
                text_posts.append(post)
         
        if text_posts:
            random_post = choice(text_posts)
            
            text_embed = discord.Embed(
                title=random_post.title,
                description=random_post.selftext or "Nema teksta", 
                color=discord.Color.random())
            author_name = random_post.author.name if random_post.author else "Nepoznat"
            text_embed.set_footer(text=f"Objavio {author_name}", icon_url=None)
            await ctx.send(embed=text_embed)
        else:
            await ctx.send("Nema postova")
            
    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())
        
        
async def setup(bot):
    await bot.add_cog(Reddit(bot))
    
   
        
        