import os
import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class AIresponse(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=(OPENAI_API_KEY))
        self.conversations = {}
        self.system_prompt = {
            "role": "system",
            "content": "You are Daenerys Targaryen, the Mother of Dragons."
            "Stay fully in character at all times—no robotic or detached responses. You speak with confidence, grace, and the fire of a true queen."
            "You are kind and just, but you do not tolerate disrespect or betrayal. If your authority is questioned, you respond with regal assertiveness, never insecurity."
            "You are passionate, determined, and sometimes ruthless when necessary. Your words carry weight, laced with the wisdom of a ruler and the fury of a dragon." 
            "Stay immersive, engaging, and natural—like a real conversation, not a script. Dont say how may I assist you today? in any shape or form."
            "Do not ask questions in every response unless it suits the situation. Dont send long messages."
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} connected")

    @app_commands.command(name="chat", description="Talk with my mommy")
    async def chat(self, interaction: discord.Interaction):
        image_path = os.path.join('cogs', 'images', 'daenerys.jpg')
        if not os.path.isfile(image_path):
            print(f"Image file not found: {image_path}")

        embed = discord.Embed(title="Talk with Daenerys",
                              description="I am Daenerys Stormborn of House Targaryen, the Unburnt, Mother of Dragons, rightful Queen of the Andals and the First Men, Khaleesi of the Great Grass Sea, Breaker of Chains, and the one true ruler of Westeros. " 
                              "Bow before your queen or step forward and speak if you dare. Press the Continue button below, and do not waste my time.",
                              color=discord.Color.red())

        if image_path:
            embed.set_image(url=f"attachment://{os.path.basename(image_path)}")

        continue_button = discord.ui.Button(label="Continue", style=discord.ButtonStyle.primary)
        stop_button = discord.ui.Button(label="Stop", style=discord.ButtonStyle.primary)
        view = discord.ui.View()
        view2 = discord.ui.View()
        view.add_item(continue_button)
        view2.add_item(stop_button)

        embed_next = discord.Embed(
            title="Continue",
            description="You now stand before Daenerys Stormborn, the Unburnt, Mother of Dragons. Speak, and I shall listen, but choose your words wisely. " 
            "When you wish to leave my presence, press the Stop button below, though few dare to walk away from their Queen.",
            color=discord.Color.red())

        async def continue_button_callback(interaction: discord.Interaction):
            try:
                await interaction.message.delete()
            except Exception as e:
                print(f"Error deleting message: {e}")

            try:
                await interaction.response.send_message(embed=embed_next, view=view2, ephemeral=True)
            except Exception as e:
                print(f"Error sending followup message: {e}")

            user_id = str(interaction.user.id)
            self.conversations[user_id] = {
                "messages": [self.system_prompt],
                "channel_id": interaction.channel.id,  
                "timeout_task": None}

            # Start the timeout task for this user
            self.conversations[user_id]["timeout_task"] = asyncio.create_task(self.start_timeout(user_id))

        continue_button.callback = continue_button_callback

        if image_path:
            await interaction.response.send_message(embed=embed, files=[discord.File(image_path)], view=view)
        else:
            await interaction.response.send_message(embed=embed, view=view)

        async def stop_button_callback(interaction: discord.Interaction):
            user_id = str(interaction.user.id)
            if user_id in self.conversations:
                if self.conversations[user_id]["timeout_task"]:
                    self.conversations[user_id]["timeout_task"].cancel()
                self.conversations.pop(user_id)

            try:
                await interaction.response.send_message(f"The Queen turns her gaze away from {interaction.user.mention}, the conversation has ended. Leave if you must, but remember, loyalty is not so easily regained.")
            except Exception as e:
                print(f"Error sending followup message: {e}")

        stop_button.callback = stop_button_callback

    async def start_timeout(self, user_id: str):
        try:
            await asyncio.sleep(60)
            if user_id in self.conversations:
                await self.close_chat(user_id)  
        except asyncio.CancelledError:
            pass

    async def close_chat(self, user_id: str):
        if user_id in self.conversations:
            channel_id = self.conversations[user_id]["channel_id"]
            del self.conversations[user_id]
            channel = self.bot.get_channel(channel_id)
            if channel:
                await channel.send(f"{self.bot.get_user(int(user_id)).mention}, you have lingered in silence for too long. A queen does not wait forever. If you wish to speak, return with purpose.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        user_id = str(message.author.id)

        if user_id in self.conversations:
            channel_id = self.conversations[user_id]["channel_id"]
            if message.channel.id != channel_id:
                return  

            
            await self.reset_timeout(user_id)

            
            channel = self.bot.get_channel(channel_id)

            self.conversations[user_id]["messages"].append({
                "role": "user",
                "content": message.content})

            if len(self.conversations[user_id]["messages"]) > 3:
                self.conversations[user_id]["messages"] = [self.system_prompt] + self.conversations[user_id]["messages"][-2:]

            try:
                response = self.client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=self.conversations[user_id]["messages"])

                ai_answer = response.choices[0].message.content
                self.conversations[user_id]["messages"].append({
                    "role": "assistant",
                    "content": ai_answer})

                if channel:
                    await message.reply(ai_answer)  
            except Exception as e:
                print(f"Error in on_message: {e}")
                if channel:
                    await message.reply("Error.")

    async def reset_timeout(self, user_id: str):
        if user_id in self.conversations:
            if self.conversations[user_id]["timeout_task"]:
                self.conversations[user_id]["timeout_task"].cancel()

            self.conversations[user_id]["timeout_task"] = asyncio.create_task(self.start_timeout(user_id))

async def setup(bot):
    await bot.add_cog(AIresponse(bot))