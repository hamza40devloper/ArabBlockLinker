import discord
from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("🛡️ Admin Module Ready.")

    # الاستماع للرسائل في قناة الـ Console لإرسالها كماين كرافت كومانند
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
            
        # TODO: التحقق مما إذا كانت الرسالة في قناة الـ Console الخاصة بالسيرفر
        # إذا بدأت بـ / يتم إرسالها كأمر لكونسول ماين كرافت
        # غير ذلك، يتم إرسالها كإعلان (Announcement) في اللعبة
        pass

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
