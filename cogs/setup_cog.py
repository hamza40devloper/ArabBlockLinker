import discord
from discord.ext import commands
from discord import app_commands

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("⚙️ Setup Module Ready.")

    @app_commands.command(name="setup", description="إتمام عملية الربط وإثبات الملكية وتوليد قنوات الإدارة")
    @app_commands.describe(code="الكود المكون من 6 أرقام الموجود في كونسول ماين كرافت")
    # قصر استخدام الأمر على من يمتلك صلاحية إدارة السيرفر فقط
    @app_commands.checks.has_permissions(administrator=True) 
    async def setup_server(self, interaction: discord.Interaction, code: str):
        
        # استدعاء المتغير العام من الملف الرئيسي لمطابقة الكود
        from main import pending_setups
        
        # 1. التحقق من صحة الكود
        if code not in pending_setups:
            await interaction.response.send_message(
                "❌ **الكود غير صحيح أو منتهي الصلاحية!** تأكد من الكونسول وأعد المحاولة.", 
                ephemeral=True
            )
            return
            
        server_ip = pending_setups[code]
        guild = interaction.guild
        
        await interaction.response.send_message("⏳ **جاري توثيق الملكية وبناء مركز الإدارة...**", ephemeral=True)
        
        try:
            # 2. إنشاء قسم الإدارة (Category) المخفي عن اللاعبين العاديين
            admin_role = interaction.user.top_role
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True, manage_channels=True),
                admin_role: discord.PermissionOverwrite(read_messages=True)
            }
            
            category = await guild.create_category("🛡️ ArabBlock Admin Hub", overwrites=overwrites)
            
            # 3. إنشاء القنوات الأربع تلقائياً داخل القسم
            await guild.create_text_channel("💻-التحكم", category=category)
            await guild.create_text_channel("📜-السجلات", category=category)
            await guild.create_text_channel("📊-الأداء", category=category)
            await guild.create_text_channel("🚨-الأمن", category=category)
            
            # 4. مسح الكود من الذاكرة لعدم استخدامه مرة أخرى
            del pending_setups[code]
            
            # 5. رسالة النجاح
            success_msg = (
                f"✅ **تم الربط بنجاح!**\n"
                f"🌐 **السيرفر المرتبط:** `{server_ip}`\n"
                f"👑 **المالك:** {interaction.user.mention}\n"
                f"تم بناء قنوات الإدارة الذاتية، يمكنك الآن إرسال الأوامر مباشرة من قناة `💻-التحكم`."
            )
            await interaction.edit_original_response(content=success_msg)
            
        except Exception as e:
            await interaction.edit_original_response(content=f"❌ **حدث خطأ أثناء بناء القنوات:** `{e}`")

async def setup(bot):
    await bot.add_cog(SetupCog(bot))
