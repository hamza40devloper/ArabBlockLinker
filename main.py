import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# 1. تحميل المتغيرات البيئية بأمان
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    raise ValueError("❌ خطأ: لم يتم العثور على توكن البوت في ملف .env")

# 2. إعداد الصلاحيات (Intents)
intents = discord.Intents.default()
intents.message_content = True  # ضروري لقراءة رسائل الشات
intents.members = True          # ضروري لإرسال رسائل خاصة (DM) في نظام الـ 2FA
intents.guilds = True

# 3. تهيئة البوت
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

# 4. دالة التحميل الديناميكي للـ Cogs
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                # اقتطاع امتداد .py لتحميل الوحدة
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"✅ Loaded: {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

# 5. أحداث البوت (Events)
@bot.event
async def on_ready():
    # مزامنة أوامر السلاش (Slash Commands) مع سيرفر الديسكورد
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")
        
    print('-----------------------------------------')
    print(f'🚀 Engine Online! Logged in as {bot.user.name}')
    # إضافة حالة احترافية (Presence)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ArabBlock Server 🛡️"))

# 6. نقطة الإطلاق (Entry Point)
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
