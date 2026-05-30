import discord
from discord.ext import commands
import json
import os

class AdminChannelsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # دالة مساعدة لإنشاء القنوات تلقائياً بعد نجاح الـ Setup
    async def create_admin_system(self, guild: discord.Guild):
        # 1. إعداد صلاحيات خاصة: إخفاء القسم عن الجميع وإظهاره للأونر والإداريين فقط
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False), # مخفي عن الأعضاء
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True) # البوت يرى ويتحكم
        }
        
        # 2. إنشاء القسم الرئيسي (Category)
        category_name = "🛡️ إدَارَة ARABBLOCK"
        category = await guild.create_category(name=category_name, overwrites=overwrites)
        print(f"📁 [Admin] تم إنشاء قسم الإدارة بنجاح في سيرفر: {guild.name}")

        # 3. إنشاء القنوات الأربعة المطلوبة داخل القسم
        channels_to_create = {
            "💻-التحكم-console": "هنا يمكنك إرسال الأوامر مباشرة إلى السيرفر (ابدأ الأمر بـ /) أو التحدث مع اللاعبين.",
            "📜-شات-البلوجينات": "تستقبل هذه القناة جميع الإشعارات والتقارير الصادرة من بلوجينات ماين كرافت.",
            "📊-مراقبة-الأداء": "تحذيرات تلقائية عند انخفاض الـ TPS أو اقتراب امتلاء ذاكرة الرام (RAM).",
            "🚨-السجلات-الأمنية": "تسجيل محاولات الدخول الخاطئة، الكلمات الممنوعة، وشبهات الهاك."
        }

        created_channels = {}
        for name, topic in channels_to_create.items():
            channel = await guild.create_text_channel(name=name, category=category, topic=topic)
            created_channels[name] = channel.id
            
            # إرسال رسالة ترحيبية وتوضيحية في كل قناة
            embed = discord.Embed(
                title=f"نظام الإدارة التلقائي لـ ArabBlock",
                description=topic,
                color=discord.Color.red()
            )
            embed.set_footer(text="Aternod Bot v2.0.1 • نظام الحماية والربط")
            await channel.send(embed=embed)

        # 4. حفظ أيدي (IDs) القنوات في ملف config.json لكي يعرف البوت أين يرسل البيانات لاحقاً
        if os.path.exists("config.json"):
            with open("config.json", "r", encoding="utf-8") as f:
                config_data = json.load(f)
        else:
            config_data = {}

        config_data["admin_channels"] = created_channels
        
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)

        return category

# دالة التحميل الأساسية
async def setup(bot):
    await bot.add_cog(AdminChannelsCog(bot))
