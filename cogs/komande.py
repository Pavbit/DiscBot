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
        ping_embed = discord.Embed(title="test", description="opet", color=discord.Color.green())
        ping_embed.add_field(name=f"{self.bot.user.name}", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        ping_embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
        await ctx.send(embed=ping_embed)

    @commands.command()
    async def embedd(self, ctx):
        embedd_embed = discord.Embed(title="Ime", description="Opis", color=discord.Color.random())
        embedd_embed.set_thumbnail(url=ctx.author.avatar)
        embedd_embed.add_field(name="test", value="opet", inline=False)
        embedd_embed.set_image(url=ctx.guild.icon)
        embedd_embed.set_footer(text="posle ce biti nes", icon_url=ctx.author.avatar)
        await ctx.send(embed=embedd_embed)


async def setup(bot):
    await bot.add_cog(Komande(bot))