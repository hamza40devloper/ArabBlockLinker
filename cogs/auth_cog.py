import discord
from discord.ext import commands
from discord import app_commands
import random
import string

class AuthCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # أمر مخصص لإرسال كود التحقق 2FA (يستدعيه السيرفر أو الإدارة)
    @app_commands.command(name="send_auth_code", description="إرسال كود التحقق للاعب لربط حسابه في اللعبة")
    @app_commands.default_permissions(administrator=True)
    async def send_auth(self, interaction: discord.Interaction, member: discord.Member, mc_username: str):
        
        # إنشاء كود عشوائي من 6 أرقام
        auth_code = ''.join(random.choices(string.digits, k=6))
        
        # تصميم الرسالة الخاصة (DM) التي ستصل للاعب
        embed = discord.Embed(
            title="🔐 ربط حساب ماين كرافت (2FA)",
            description=f"أهلاً بك في سيرفر ArabBlock!\n\n"
                        f"لقد تم طلب ربط حسابك بالاسم: `{mc_username}`\n"
                        f"كود التحقق الخاص بك هو: **{auth_code}**\n\n"
                        f"⚠️ **لديك 5 دقائق** لكتابة هذا الكود في شات اللعبة، وإلا سيتم طردك.\n"
                        f"بعد الإدخال الصحيح، سيُطلب منك إنشاء كلمة سر باستخدام `/register`.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="يرجى عدم مشاركة هذا الكود مع أي شخص.")

        try:
            # إرسال الرسالة الخاصة للاعب
            await member.send(embed=embed)
            await interaction.response.send_message(f"✅ تم إرسال الكود `{auth_code}` بنجاح في الخاص للعضو {member.mention}.", ephemeral=True)
            
            # (هنا في النظام الفعلي يتم حفظ الكود في ملف أو قاعدة بيانات ليقرأه بلوجين ماين كرافت)
            
        except discord.Forbidden:
            # في حال كان اللاعب مقفلاً رسائله الخاصة
            await interaction.response.send_message(f"❌ لم أتمكن من إرسال الرسالة. يبدو أن {member.mention} قد أغلق الرسائل الخاصة (DMs).", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AuthCog(bot))
