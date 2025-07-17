import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
# Load environment variables
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

intents = discord.Intents.default()
intents.members = True           # if you need member info
intents.voice_states = True      # crucial for voice‐state events

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_voice_state_update(member, before, after):
    log_ch = member.guild.get_channel(LOG_CHANNEL_ID)
    if not log_ch:
        return  # channel not found

    # Join event
    if before.channel is None and after.channel is not None:
        await log_ch.send(f":green_circle: **{member.display_name}** joined voice channel **{after.channel.name}**")
    # Leave event
    elif before.channel is not None and after.channel is None:
        await log_ch.send(f":red_circle: **{member.display_name}** left voice channel **{before.channel.name}**")
    # Switch channels
    elif before.channel is not None and after.channel is not None and before.channel != after.channel:
        await log_ch.send(
            f":left_right_arrow: **{member.display_name}** moved from **{before.channel.name}** to **{after.channel.name}**"
        )

bot.run(BOT_TOKEN)