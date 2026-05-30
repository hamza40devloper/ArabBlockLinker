import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from aiohttp import web

# 1. تحميل المتغيرات البيئية
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PORT = int(os.getenv('PORT', 8080))
API_KEY = os.getenv('API_KEY') # جلب مفتاح الأمان للتحقق من طلبات البلوجين

if not TOKEN:
    raise ValueError("❌ خطأ: لم يتم العثور على توكن البوت.")

# 2. إعداد الصلاحيات
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

# ----------------- متغيرات النظام (Global Variables) -----------------
# متغير عام لحفظ أكواد الـ Setup المؤقتة القادمة من السيرفر
pending_setups = {}

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

# نقطة استقبال كود التوثيق (Setup) من بلوجين ماين كرافت
async def handle_init_setup(request):
    try:
        # التحقق من مفتاح الأمان (Security Check) لمنع الطلبات الوهمية
        auth_header = request.headers.get('Authorization')
        if auth_header != API_KEY:
            return web.json_response({"error": "Unauthorized Access"}, status=401)
        
        # استلام البيانات من البلوجين
        data = await request.json()
        server_ip = data.get('ip')
        setup_code = data.get('code')
        
        if not server_ip or not setup_code:
            return web.json_response({"error": "Missing parameters"}, status=400)
            
        # حفظ الكود مؤقتاً في ذاكرة البوت
        pending_setups[str(setup_code)] = server_ip
        print(f"📥 Received setup code {setup_code} from {server_ip}")
        
        return web.json_response({"status": "success", "message": "Code received"}, status=200)
        
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

# دالة تشغيل خادم الويب الخاص بالجسر
async def start_web_server():
    app = web.Application()
    
    # دمج وتعيين جميع المسارات (Endpoints) هنا
    app.router.add_post('/api/auth', handle_auth_request)
    app.router.add_post('/api/init_setup', handle_init_setup)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # الاستماع على التردد 0.0.0.0 وهو ضروري لبيئة تشغيل Railway
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f"🌐 Communication Bridge Online on port {PORT}")

# ----------------- تجهيز وإطلاق البوت (Bot Setup) -----------------

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

# 4. نقطة الإطلاق المشتركة (Entry Point)
async def main():
    async with bot:
        await load_cogs()
        # تشغيل خادم الويب في الخلفية بالتزامن مع البوت
        await start_web_server()
        # بدء تشغيل البوت
        await bot.start(TOKEN)

# التأكد من تشغيل الملف مباشرة وليس عبر استدعاء خارجي
if __name__ == '__main__':
    asyncio.run(main())
