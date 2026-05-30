import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# تحميل المتغيرات البيئية (للحماية)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# إعداد صلاحيات البوت (Intents) لسماع الرسائل وقراءة الأعضاء
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# إنشاء البوت (سنستخدم الـ Slash Commands لاحقاً، لكن هذه البادئة كلاسيكية)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user.name}')
    print(f'🌐 Bot is online and ready for ArabBlock!')
    
    # هنا سنقوم بتحميل ملفات الـ Cogs لاحقاً بمجرد إنشائها
    # await bot.load_extension('cogs.setup_cog')

# تشغيل البوت
if __name__ == '__main__':
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ Error: DISCORD_TOKEN not found! Please check your .env file or Railway variables.")
