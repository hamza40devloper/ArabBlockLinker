import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import json
import os

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # تعريف أمر السلاش وتحديد أنه مسموح للإداريين فقط
    @app_commands.command(name="setup", description="ربط وتفعيل بوت ArabBlock بسيرفر ماين كرافت")
    @app_commands.default_permissions(administrator=True) 
    async def setup_command(self, interaction: discord.Interaction, ip: str, port: int):
        
        # 1. إرسال رسالة للمستخدم تطلب منه الكود
        await interaction.response.send_message(
            f"🔄 جاري التحضير لربط السيرفر `{ip}:{port}`...\n"
            f"👀 يرجى التحقق من كونسول سيرفر ماين كرافت الآن، لقد تم إصدار **كود تحقق من 6 أرقام**.\n"
            f"⌨️ قم بكتابة الكود هنا في الشات خلال **60 ثانية**:",
            ephemeral=True # هذه تجعل الرسالة تظهر للمستخدم فقط ولا يراها غيره
        )

        # 2. وظيفة للتأكد أن الرسالة القادمة هي من نفس الشخص وفي نفس القناة
        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel

        try:
            # 3. انتظار إدخال الكود لمدة 60 ثانية
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            code = msg.content.strip()

            # (محاكاة للتحقق: لاحقاً سنربطها بقاعدة البيانات أو API البلوجين للتأكد من تطابق الكود)
            # حالياً سنتحقق فقط من أن الإدخال عبارة عن 6 أرقام
            if len(code) == 6 and code.isdigit():
                
                # 4. حفظ بيانات السيرفر في ملف JSON محلي
                config_data = {
                    "server_ip": ip,
                    "server_port": port,
                    "is_setup": True,
                    "owner_id": interaction.user.id
                }
                
                # إنشاء ملف config.json لحفظ الإعدادات
                with open("config.json", "w", encoding="utf-8") as f:
                    json.dump(config_data, f, indent=4)

                await interaction.followup.send(f"✅ **تم التحقق بنجاح!** تمت تهيئة سيرفر ArabBlock وتم ربطه بحسابك.", ephemeral=True)
                
                # حذف رسالة الكود التي أرسلها المالك للحفاظ على الأمان ونظافة الشات
                await msg.delete()
                
            else:
                await interaction.followup.send("❌ **كود غير صالح!** يجب أن يتكون الكود من 6 أرقام صحيحة. أعد المحاولة بكتابة `/setup`.", ephemeral=True)

        except asyncio.TimeoutError:
            # في حال مرت 60 ثانية ولم يكتب شيئاً
            await interaction.followup.send("⏳ **انتهى الوقت!** لم تقم بإدخال الكود المكون من 6 أرقام. أعد المحاولة بكتابة `/setup`.", ephemeral=True)


# دالة أساسية لتحميل الملف (Cog) داخل البوت
async def setup(bot):
    await bot.add_cog(SetupCog(bot))
