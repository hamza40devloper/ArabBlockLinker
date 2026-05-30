import discord
from discord.ext import commands
import random
import asyncio

class AuthCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("🔐 2FA Auth Module Ready.")

    # دالة سيتم استدعاؤها من الماين كرافت عبر API عندما يطلب اللاعب كود التحقق
    async def send_auth_code(self, discord_user_id: int):
        user = self.bot.get_user(discord_user_id)
        if user:
            code = random.randint(100000, 999999)
            # TODO: إرسال الكود في رسالة خاصة (DM) وحفظه مؤقتاً لمطابقته
            try:
                await user.send(f"🔑 كود التحقق الخاص بك هو: **{code}**\nلديك 5 دقائق لإدخاله في السيرفر.")
            except discord.Forbidden:
                print(f"❌ لا يمكن إرسال رسالة خاصة للمستخدم {discord_user_id} (ربما قام بإغلاق الـ DMs)")

async def setup(bot):
    await bot.add_cog(AuthCog(bot))
