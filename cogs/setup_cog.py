import discord
from discord.ext import commands
from discord import app_commands

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("⚙️ Setup Module Ready.")

    @app_commands.command(name="setup", description="ربط سيرفر ماين كرافت وإثبات الملكية")
    @app_commands.describe(ip="آي بي سيرفر ماين كرافت", port="البورت الخاص بالسيرفر")
    async def setup_server(self, interaction: discord.Interaction, ip: str, port: int):
        # TODO: الاتصال بـ API الماين كرافت لإنشاء كود التوثيق (6 أرقام)
        await interaction.response.send_message(f"⏳ جاري محاولة الاتصال بالسيرفر {ip}:{port} لإنشاء كود التوثيق...", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SetupCog(bot))
