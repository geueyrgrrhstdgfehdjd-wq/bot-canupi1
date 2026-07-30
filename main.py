import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# โหลดค่า Token จากไฟล์ .env (สำหรับรันในเครื่อง)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class IssueSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="ยศไม่เข้า",
                description="แจ้งปัญหากรณีซื้อยศแล้วยศไม่ขึ้น",
                emoji="👑",
                value="role_issue"
            ),
            discord.SelectOption(
                label="บอทใช้ไม่ได้",
                description="แจ้งปัญหากรณีบอทเปิดไม่ติด/ไม่อ่านคำสั่ง",
                emoji="🤖",
                value="bot_issue"
            ),
            discord.SelectOption(
                label="เงินไม่เข้า",
                description="แจ้งปัญหากรณีเติมเงินแล้วยอดเงินไม่ปรับ",
                emoji="💰",
                value="money_issue"
            ),
        ]
        super().__init__(
            placeholder="เลือกประเภทปัญหาที่พบ...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        if selected == "role_issue":
            await interaction.response.send_message("คุณได้เลือกแจ้งปัญหา: **ยศไม่เข้า** (กรุณารอทีมงานตรวจสอบ)", ephemeral=True)
        elif selected == "bot_issue":
            await interaction.response.send_message("คุณได้เลือกแจ้งปัญหา: **บอทใช้ไม่ได้** (กรุณารอทีมงานตรวจสอบ)", ephemeral=True)
        elif selected == "money_issue":
            await interaction.response.send_message("คุณได้เลือกแจ้งปัญหา: **เงินไม่เข้า** (กรุณารอทีมงานตรวจสอบ)", ephemeral=True)

class IssueView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(IssueSelect())

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f'ล็อกอินเรียบร้อยแล้วในชื่อ: {bot.user.name}')

@bot.tree.command(name="setup", description="ตั้งค่าระบบแจ้งปัญหา")
async def setup(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚠️ กฎระเบียบและจุดแจ้งปัญหา ⚠️",
        color=discord.Color.red()
    )
    embed.description = (
        "• **ห้ามเปิดเล่น เปิดเล่น = แบน**\n"
        "• **เฉพาะแจ้งปัญหาเท่านั้น**\n"
        "• **ถ้ามีเรื่องอื่นให้ทักส่วนตัว**"
    )
    image_url = "https://cdn.discordapp.com/attachments/1532407293872701593/1532415384073015407/C9212D81-9C91-4D01-AD71-DC4F8200AA6D.png?ex=6a6cc48a&is=6a6b730a&hm=0a256502ce3389f9e309cdeb8edaef49dc805037bbc0aac13809f8ca661e8138&"
    embed.set_image(url=image_url)

    await interaction.response.send_message(embed=embed, view=IssueView())

# ดึง Token จาก Environment Variable เพื่อความปลอดภัย
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
