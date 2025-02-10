import discord
from discord.ext import commands
class Komande(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online")
        

    @commands.command()
    async def ping(self, ctx):
        bot_avatar = getattr(self.bot.user, "avatar_url", self.bot.user.avatar)
        creation_date = self.bot.user.created_at.strftime("%Y-%m-%d") #konvertuje datum u string
        
        ping_embed = discord.Embed(title="O botu", description=f"Bot nastao {creation_date}", 
                                   color=discord.Color.green())
        ping_embed.set_thumbnail(url=str(bot_avatar))
        ping_embed.add_field(name=f"{self.bot.user.name}", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        ping_embed.set_footer(text=f"Obavljeno od strane {ctx.author.name}", icon_url=ctx.author.avatar)
        await ctx.send(embed=ping_embed)

    @commands.command()
    async def info(self, ctx):
        creation_date = ctx.guild.created_at.strftime("%Y-%m-%d") #konvertuje datum u string
        
        info_embed = discord.Embed(title=ctx.guild.name, 
            description=f"Server ima {ctx.guild.member_count} ljudi.", color=discord.Color.random())
        info_embed.set_thumbnail(url=ctx.author.avatar)
        info_embed.add_field(name="Datum nastanka", value=creation_date, inline=False)
        info_embed.set_image(url=ctx.guild.icon)
        info_embed.set_footer(text=f"Obavljeno od strane {ctx.author.name}", icon_url=ctx.author.avatar)
        await ctx.send(embed=info_embed)

    @commands.command()
    async def user(self, ctx):
        await ctx.send("Unesi ime: ")
        if " message" == self.bot.user:
            return
        name = await self.bot.wait_for("message")
        await ctx.send(f"Poz {name.content}")
     


async def setup(bot):
    await bot.add_cog(Komande(bot))
    
