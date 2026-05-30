import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from aiohttp import web  # استيراد مكتبة الويب للربط مع البلوجين

# 1. تحميل المتغيرات البيئية
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# Railway تمنحك منفذ ديناميكي تلقائياً عبر المتغير PORT، ونضع 8080 كافتراضي للمحلي
PORT = int(os.getenv('PORT', 8080)) 

if not TOKEN:
    raise ValueError("❌ خطأ: لم يتم العثور على توكن البوت.")

# 2. إعداد الصلاحيات
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

# ----------------- جسر الاتصال مع البلوجين (API Routes) -----------------

# نقطة استقبال لطلب كود الـ 2FA من اللعبة
async def handle_auth_request(request):
    try:
        data = await request.json()
        discord_id = int(data.get('discord_id'))
        # استدعاء دالة إرسال الكود الموجودة في الـ Cog الخاص بالحماية
        auth_cog = bot.get_cog('AuthCog')
        if auth_cog:
            asyncio.create_task(auth_cog.send_auth_code(discord_id))
            return web.json_response({"status": "success", "message": "Code sent via DM"}, status=200)
        return web.json_response({"status": "error", "message": "Auth module not ready"}, status=500)
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=400)

# دالة تشغيل خادم الويب الخاص بالجسر
async def start_web_server():
    app = web.Application()
    # تعيين المسارات (Endpoints) التي سيتصل بها بلوجين الجافا
    app.router.add_post('/api/auth', handle_auth_request)
    
    runner = web.AppRunner(app)
    await runner.setup()
    # الاستماع على التردد 0.0.0.0 وهو ضروري لبيئة تشغيل Railway
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f"🌐 Communication Bridge Online on port {PORT}")

# ---------------------------------------------------------------------

# 3. دالة التحميل الديناميكي للـ Cogs
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"✅ Loaded: {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")
        
    print('-----------------------------------------')
    print(f'🚀 Engine Online! Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ArabBlock Server 🛡️"))

# 4. نقطة الإطلاق المشتركة
async def main():
    async with bot:
        await load_cogs()
        # تشغيل خادم الويب في الخلفية بالتزامن مع البوت
        await start_web_server()
        # بدء تشغيل البوت
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
