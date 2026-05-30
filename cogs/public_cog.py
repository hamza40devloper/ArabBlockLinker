import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class PublicChannelsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "server_data.json"

    # أمر لإضافة عنصر جديد إلى المتجر الحي
    @app_commands.command(name="add_store_item", description="إضافة أداة أو عنصر جديد لمتجر السيرفر")
    @app_commands.default_permissions(administrator=True)
    async def add_item(self, interaction: discord.Interaction, item_name: str, price: str, image_url: str = None):
        embed = discord.Embed(
            title=f"🛒 متجر ArabBlock | {item_name}",
            description=f"**السعر:** `{price}` داخل اللعبة.",
            color=discord.Color.gold()
        )
        if image_url:
            embed.set_image(url=image_url)
        embed.set_footer(text="Aternod Bot | المتجر المباشر")
        
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("✅ تم إرسال العنصر إلى المتجر بنجاح.", ephemeral=True)

    # أمر لتحديث عدد الكلات (يمكن ربطه لاحقاً بـ API من ماين كرافت لتحديثه تلقائياً)
    @app_commands.command(name="update_kills", description="تحديث لوحة شرف الكلات")
    @app_commands.default_permissions(administrator=True)
    async def update_kills(self, interaction: discord.Interaction, player_name: str, kills: int):
        # في النظام الحقيقي سيتم قراءة البيانات من ملف JSON أو قاعدة بيانات
        embed = discord.Embed(
            title="🏆 لوحة شرف المتصدرين (Live Kills)",
            description=f"**المركز الأول الحالي:**\n⚔️ `{player_name}` - {kills} Kills",
            color=discord.Color.dark_red()
        )
        embed.set_footer(text="يتم التحديث تلقائياً مع كل قتلة داخل السيرفر")

        # التحقق مما إذا كانت هناك رسالة سابقة لتعديلها بدلاً من إرسال رسالة جديدة
        # (لتبسيط الكود، نرسلها كرسالة جديدة هنا، وفي التطوير المتقدم نستخدم message.edit)
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message(f"✅ تم تحديث اللوحة للاعب {player_name}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(PublicChannelsCog(bot))
