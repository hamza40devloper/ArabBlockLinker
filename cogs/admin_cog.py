import discord
from discord.ext import commands
import json
import os

class AdminChannelsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_admin_system(self, guild: discord.Guild):
        # إعداد الصلاحيات: القسم مخفي عن الأعضاء، ظاهر فقط للمالك والإداريين
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }
        
        # إنشاء القسم الرئيسي
        category = await guild.create_category(name="🛡️ إدَارَة ARABBLOCK", overwrites=overwrites)
        
        # تعريف القنوات مع وصفها
        channels_info = {
            "💻-التحكم-console": "هنا يمكنك إرسال الأوامر مباشرة إلى السيرفر (ابدأ بـ /).",
            "📜-شات-البلوجينات": "سجلات وتقارير البلوجينات داخل السيرفر.",
            "📊-مراقبة-الأداء": "إشعارات حول الـ TPS واستهلاك الرام.",
            "🚨-السجلات-الأمنية": "سجلات الدخول الخاطئ والكلمات الممنوعة."
        }

        created_channels = {}
        for name, topic in channels_info.items():
            channel = await guild.create_text_channel(name=name, category=category, topic=topic)
            created_channels[name] = channel.id
            
            # إرسال رسالة ترحيبية احترافية في كل قناة
            embed = discord.Embed(
                title=f"قناة {name}",
                description=f"**الوظيفة:** {topic}\n\nهذه القناة محمية ومخصصة لإدارة سيرفر ArabBlock.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Aternod Bot v2.0.1 | نظام الإدارة التلقائي")
            await channel.send(embed=embed)

        # حفظ أيدي القنوات في config.json
        config_path = "config.json"
        data = {}
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        
        data["admin_channels"] = created_channels
        
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        
        print(f"✅ [Admin] تم إنشاء قسم الإدارة والقنوات بنجاح في {guild.name}")
        return category

async def setup(bot):
    await bot.add_cog(AdminChannelsCog(bot))
