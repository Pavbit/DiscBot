import discord
from discord.ext import commands
import os
import random
from easy_pil import Editor, load_image_async, Font

class MemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} povezan")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):  

        welcome_channel = member.guild.system_channel
        if not welcome_channel:
            print("Nije pronadjen kanal za dobrodoslicu")
            return
        
        welcome_messages = [
            f"All hail {member.mention}! A new protector of the realm has arrived to fortify the walls of {member.guild.name}!",
            f"The banners are raised, the horns sound! {member.mention} has entered the court of {member.guild.name}. May they serve with honor!",
            f"The gates of {member.guild.name} open wide as {member.mention} rides forth to claim their place as the #{member.guild.member_count} protector of the realm!"
        ]
        
        images_path = "./cogs/welcomemember_images"
        if not os.path.exists(images_path):
            print("Nije pronadjen folder sa slikama")
            return

        images = os.listdir(images_path)
        if not images:
            print("Nisu pronadjene slike")
            return

        randomized_welcome = random.choice(welcome_messages)
        randomized_image = random.choice(images)

        try:
            bg = Editor(f"{images_path}/{randomized_image}").resize((1920, 1080))
        except Exception as e:
            print(f"Nije ucitana slika {e}")
            return


        try:
            avatar_image = await load_image_async(str(member.avatar.url))
            avatar = Editor(avatar_image).resize((250, 250))
            avatar = avatar.circle_image()  
        except Exception as e:
            print(f"Nije ucitan avatar {e}")
            return


        font_big_path = "./cogs/welcomemember_fonts/Poppins-Bold.ttf"
        font_small_path = "./cogs/welcomemember_fonts/Poppins-Regular.ttf"
        
        
        if not os.path.exists(font_big_path or font_small_path):
            print("Nisu pronadjeni fontovi")
            return

        font_big = Font(font_big_path, size=90)
        font_small = Font(font_small_path, size=60)

        
        bg.paste(avatar, (835, 340))
        bg.ellipse((835, 340), 250, 250, outline="white", stroke_width=5)
        bg.text((960, 620), f"The Realm Welcomes {member.name}!", color="white", font=font_big, align="center")
        bg.text((960, 740), f"Now among the {member.guild.member_count} sworn protectors of {member.guild.name}", 
                color="white", font=font_small, align="center") 


        image_bytes = bg.image_bytes
        image_file = discord.File(fp=image_bytes, filename="welcome.png")

       
        await welcome_channel.send(f"{randomized_welcome}")
        await welcome_channel.send(file=image_file)


async def setup(bot):
    await bot.add_cog(MemberJoin(bot))