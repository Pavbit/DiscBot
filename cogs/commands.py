import discord
from discord import app_commands
from discord.ext import commands
class Commands(commands.Cog):
    
    
    def __init__(self, bot):
        self.bot = bot

    commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online")
        

    @app_commands.command(name="ping", description="Informacije bota.")
    async def ping(self, interaction: discord.Interaction):
        bot_avatar = getattr(self.bot.user, "avatar_url", self.bot.user.avatar)
        creation_date = self.bot.user.created_at.strftime("%Y-%m-%d") #konvertuje datum u string
        
        ping_embed = discord.Embed(title="O botu", description=f"Bot nastao {creation_date}", 
                                   color=discord.Color.green())
        ping_embed.set_thumbnail(url=str(bot_avatar))
        ping_embed.add_field(name=f"{self.bot.user.name}", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        ping_embed.set_footer(text=f"Obavljeno od strane {interaction.user.name}", icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=ping_embed)

    @app_commands.command(name="info", description="Informacije o serveru.")
    async def info(self, interaction: discord.Interaction):
        creation_date = interaction.guild.created_at.strftime("%Y-%m-%d") #konvertuje datum u string
        
        info_embed = discord.Embed(title=interaction.guild.name, 
            description=f"Server ima {interaction.guild.member_count} ljudi.", color=discord.Color.random())
        info_embed.set_thumbnail(url=interaction.user.avatar)
        info_embed.add_field(name="Datum nastanka", value=creation_date, inline=False)
        info_embed.set_image(url=interaction.guild.icon)
        info_embed.set_footer(text=f"Obavljeno od strane {interaction.user.name}", icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=info_embed)

    @app_commands.command(name="user", description="Pozdrav korisnika.")
    async def user(self, interaction: discord.Interaction):
        await interaction.response.send_message("Unesi ime:")
        
        def check(message: discord.Message):
            return message.author == interaction.user and message.channel == interaction.channel
        
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30)
            await interaction.followup.send(f"Poz {msg.content}")
        except Exception:
            await interaction.followup.send("Nije registrovano ime.")
     

    @app_commands.command(name="panic", description="Na panica.")
    async def panic(self, interaction: discord.Interaction):
         panic_embed = discord.Embed(title="Na Panica", description="sI pOlOzIo MeNaDzMeNt AAAA", color=discord.Color.random())
         panic_embed.set_image(url="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2dxejJicWU1cjZkMncwNnEwYXNvMGx0M3IxeW1qYmxmamZkeDVhdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ESgYN7LGXgIO4/giphy.gif")
         panic_embed.set_footer(text=f"zasluzeno ga spalio {interaction.user.name}", icon_url=interaction.user.avatar)
         await interaction.response.send_message(embed=panic_embed)
         

async def setup(bot):
    await bot.add_cog(Commands(bot))
    

