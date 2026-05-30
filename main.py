import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية للحماية
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# إعداد الصلاحيات الأساسية للبوت
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# بناء كلاس مخصص للبوت للتحكم في مرحلة الإقلاع (Startup)
class ArabBlockBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)

    # هذه الدالة تعمل تلقائياً قبل تشغيل البوت لتجهيز ملفات الميزات ومزامنة الأوامر
    async def setup_hook(self):
        # 1. تحميل ملف نظام التثبيت وإثبات الملكية
        await self.load_extension('cogs.setup_cog')
        print("📦 [Extension] تم تحميل ميزة التثبيت (setup_cog) بنجاح!")
        
        # 2. مزامنة أوامر السلاش (Slash Commands) مع سيرفرات الديسكورد لتظهر فوراً
        print("🔄 [Discord] جاري مزامنة أوامر السلاش...")
        synced = await self.tree.sync()
        print(f"✅ [Discord] تمت المزامنة بنجاح! تم تسجيل ({len(synced)}) أمر سلاش عالمي.")

# تشغيل البوت باستخدام الكلاس الجديد
bot = ArabBlockBot()

@bot.event
async def on_ready():
    print(f'===-----------------------------------------===')
    print(f'✅ تم تسجيل الدخول باسم البوت: {bot.user.name}')
    print(f'🌐 بوت ArabBlock يعمل الآن وطاقة الاتصال ممتازة!')
    print(f'===-----------------------------------------===')

# نقطة الانطلاق لتشغيل الكود بنجاح
if __name__ == '__main__':
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ خطأ: لم يتم العثور على DISCORD_TOKEN! يرجى التأكد من ملف .env أو إعدادات منصة Railway.")
