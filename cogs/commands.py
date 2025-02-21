import os
import discord
from discord import app_commands
from discord.ext import commands


class Commands(commands.Cog):
    
    
    def __init__(self, bot):
        self.bot = bot

    commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online")
        

    @app_commands.command(name="ping", description="Bot information")
    async def ping(self, interaction: discord.Interaction):
        bot_avatar = getattr(self.bot.user, "avatar_url", self.bot.user.avatar)
        creation_date = self.bot.user.created_at.strftime("%Y-%m-%d") #konvertuje datum u string
        
        ping_embed = discord.Embed(title="About bot", description=f"Bot created on {creation_date} by pavke_c, still in beta version. If you have any ideas or bug reports, feel free to use /feedback", 
                                   color=discord.Color.green())
        ping_embed.set_thumbnail(url=str(bot_avatar))
        ping_embed.add_field(name=f"{self.bot.user.name}", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        ping_embed.set_footer(text=f"Command done by {interaction.user.name}", icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=ping_embed)

    @app_commands.command(name="info", description="Basic information about the server")
    async def info(self, interaction: discord.Interaction):
        creation_date = interaction.guild.created_at.strftime("%Y-%m-%d") #konvertuje datum u string
        
        info_embed = discord.Embed(title=interaction.guild.name, 
            description=f"Server has {interaction.guild.member_count} people.", color=discord.Color.random())
        info_embed.set_thumbnail(url=interaction.user.avatar)
        info_embed.add_field(name="Date of creation", value=creation_date, inline=False)
        info_embed.set_image(url=interaction.guild.icon)
        info_embed.set_footer(text=f"Command done by {interaction.user.name}", icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=info_embed)
         
    @app_commands.command(name="feedback", description="Send a raven with your feedback or bug report to the Queen")
    async def feedback(self, interaction: discord.Interaction, message: str):
        feedback_channel_id = 1341799697760649286
        feedback_channel = self.bot.get_channel(feedback_channel_id)
        
        embed = discord.Embed(title="New Feedback Received", description=message, color=discord.Color.blue())
        embed.set_footer(text=f"Sent by {interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await feedback_channel.send(embed=embed)
        await interaction.response.send_message("Your raven has been sent to the Queen's council. Let's hope it doesn't get intercepted by Lannisters.", ephemeral=True)     
    
    
    @app_commands.command(name="invite", description="Invite the bot to your server")
    async def invite(self, interaction: discord.Interaction):
        invite_image = "./cogs/images/dragoninvite.jpg"
        invite_link = "https://discord.com/oauth2/authorize?client_id=1334985967110586441&permissions=1126451810528320&integration_type=0&scope=bot"
        
        invite_embed = discord.Embed(title="The Dragon's Call: Invite Drakonis to Your Kingdom", 
                                     description="From the ashes of the old world, the dragon rises. Invite Drakonis and rule the Seven Kingdoms!", 
                                     color=discord.Color.red())
        
        invite_embed.set_image(url="attachment://dragoninvite.jpg")
        file = discord.File(invite_image, filename="dragoninvite.jpg")
        
        invite_embed.add_field(name="Click here:", value=invite_link, inline=False)
        invite_embed.set_footer(text=f"Command done by {interaction.user.name}", icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=invite_embed, file=file)
        
    @app_commands.command(name="help", description="Displays all available commands")
    async def help(self, interaction: discord.Interaction):
        help_embed = discord.Embed(title="Available Commands", color=discord.Color.blue())
        
        for command in self.bot.tree.get_commands():
            if command.name == "help": continue
            help_embed.add_field(name=f"/{command.name}", value=command.description, inline=False)

        help_embed.set_footer(text=f"Command done by {interaction.user.name}", icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=help_embed)

async def setup(bot):
    await bot.add_cog(Commands(bot))
    

