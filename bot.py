import os
import random
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN      = os.getenv("DISCORD_TOKEN")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))
APP_ID         = int(os.getenv("APPLICATION_ID"))
GUILD_ID       = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
intents.voice_states = True

# Pass your application_id so bot.tree works
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    application_id=APP_ID
)

@bot.event
async def on_ready():
    # Register slash commands to your test guild (instant)
    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

# Your existing voice‐state logger
@bot.event
async def on_voice_state_update(member, before, after):
    log_ch = member.guild.get_channel(LOG_CHANNEL_ID)
    if not log_ch:
        return

    if before.channel is None and after.channel is not None:
        await log_ch.send(f":green_circle: **{member.display_name}** joined **{after.channel.name}**")
    elif before.channel is not None and after.channel is None:
        await log_ch.send(f":red_circle: **{member.display_name}** left **{before.channel.name}**")
    elif before.channel != after.channel:
        await log_ch.send(f":left_right_arrow: **{member.display_name}** moved from **{before.channel.name}** to **{after.channel.name}**")

# ——— New slash command ———
@bot.tree.command(
    name="coin",
    description="Flip a coin and get heads or tails",
    guild=discord.Object(id=GUILD_ID)    # for instant registration in your test server
)
async def coin(interaction: discord.Interaction):
    result = random.choice(["Heads", "Tails"])
    await interaction.response.send_message(f"🪙 You got **{result}**!")

bot.run(BOT_TOKEN)
