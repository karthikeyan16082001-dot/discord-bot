import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_BATOR = int(os.getenv("ROLE_BATOR"))
ROLE_KINKY = int(os.getenv("ROLE_KINKY"))
ROLE_BI = int(os.getenv("ROLE_BI"))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


class RoleButton(Button):
    def __init__(self, emoji: str, label: str, role_id: int):
        # Add custom_id so the button persists
        super().__init__(
            style=discord.ButtonStyle.primary,
            label=label,
            emoji=emoji,
            custom_id=str(role_id)
        )
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(self.role_id)
        if role is None:
            await interaction.response.send_message("⚠️ Role not found.", ephemeral=True)
            return

        member = interaction.user
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"❌ Removed role: {role.name}", ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(f"✅ Added role: {role.name}", ephemeral=True)


class RoleView(View):
    def __init__(self):
        # persistent = True makes it survive restarts
        super().__init__(timeout=None)
        self.add_item(RoleButton("💦", "Bator", ROLE_BATOR))
        self.add_item(RoleButton("😈", "Kinky", ROLE_KINKY))
        self.add_item(RoleButton("🔀", "Bi", ROLE_BI))


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    # Register the persistent view (no message send yet)
    bot.add_view(RoleView())

    # Only send once — check if bot is running for first time
    channel = await bot.fetch_channel(CHANNEL_ID)
    async for msg in channel.history(limit=50):
        if msg.author == bot.user and "Choose your role" in msg.content:
            print("✅ Role message already exists, skipping.")
            return

    await channel.send("Choose your role by clicking a button:", view=RoleView())


bot.run(TOKEN)
