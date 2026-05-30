import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class ArabBlockBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        # تحميل جميع ملفات النظام دفعة واحدة
        cogs_to_load = [
            'cogs.setup_cog',   # التثبيت
            'cogs.admin_cog',   # قنوات الإدارة
            'cogs.public_cog',  # المتجر واللوحة
            'cogs.auth_cog'     # نظام الـ 2FA
        ]
        
        for cog in cogs_to_load:
            try:
                await self.load_extension(cog)
                print(f"📦 تم تحميل: {cog}")
            except Exception as e:
                print(f"❌ خطأ في تحميل {cog}: {e}")
        
        print("🔄 جاري مزامنة أوامر السلاش...")
        await self.tree.sync()
        print("✅ تمت المزامنة بنجاح!")

bot = ArabBlockBot()

@bot.event
async def on_ready():
    print(f'===-----------------------------------------===')
    print(f'✅ بوت ArabBlock يعمل الآن كـ: {bot.user.name}')
    print(f'===-----------------------------------------===')

if __name__ == '__main__':
    if TOKEN:
        bot.run(TOKEN)    print(f'✅ تم تسجيل الدخول باسم البوت: {bot.user.name}')
    print(f'🌐 بوت ArabBlock يعمل الآن وطاقة الاتصال ممتازة!')
    print(f'===-----------------------------------------===')

# نقطة الانطلاق لتشغيل الكود بنجاح
if __name__ == '__main__':
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ خطأ: لم يتم العثور على DISCORD_TOKEN! يرجى التأكد من ملف .env أو إعدادات منصة Railway.")
