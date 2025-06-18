import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong !")

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

class PokemonControlView(View):
    def __init__(self):
        super().__init__(timeout=None)  # timeout=None pour que le view reste actif

    @discord.ui.button(label="⬆️ Up", style=discord.ButtonStyle.primary)
    async def up_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open("input.txt", "w") as f:
            f.write("up")
        await interaction.response.send_message("Commande UP envoyée !", ephemeral=True)

    @discord.ui.button(label="⬇️ Down", style=discord.ButtonStyle.primary)
    async def down_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open("input.txt", "w") as f:
            f.write("down")
        await interaction.response.send_message("Commande DOWN envoyée !", ephemeral=True)

    @discord.ui.button(label="⬅️ Left", style=discord.ButtonStyle.primary)
    async def left_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open("input.txt", "w") as f:
            f.write("left")
        await interaction.response.send_message("Commande LEFT envoyée !", ephemeral=True)

    @discord.ui.button(label="➡️ Right", style=discord.ButtonStyle.primary)
    async def right_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open("input.txt", "w") as f:
            f.write("right")
        await interaction.response.send_message("Commande RIGHT envoyée !", ephemeral=True)

    @discord.ui.button(label="A", style=discord.ButtonStyle.success)
    async def a_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open("input.txt", "w") as f:
            f.write("A")
        await interaction.response.send_message("Commande A envoyée !", ephemeral=True)

    @discord.ui.button(label="B", style=discord.ButtonStyle.danger)
    async def b_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open("input.txt", "w") as f:
            f.write("B")
        await interaction.response.send_message("Commande B envoyée !", ephemeral=True)

@bot.command()
async def start(ctx):
    """Envoie les boutons de contrôle Pokémon"""
    view = PokemonControlView()
    await ctx.send("Contrôle ton Pokémon avec les boutons :", view=view)

token = os.getenv('DISCORD_TOKEN')
bot.run(token)
