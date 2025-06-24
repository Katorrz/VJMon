import asyncio
import datetime
import os
import shutil
import time
import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
import pygetwindow as gw
import mss
from PIL import Image

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

import asyncio

class PokemonControlView(View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.last_message = None

    async def handle_command(self, interaction: discord.Interaction, key: str, repeat=1):
        await interaction.response.send_message(
            f"Commande {key.upper()}{' x'+str(repeat) if repeat > 1 else ''} envoyée !",
            ephemeral=True
        )

        for _ in range(repeat):
            with open("input.txt", "w") as f:
                f.write(key)
            await asyncio.sleep(0.3)

        path = capture_desmume()
        if path:
            # Envoie la nouvelle frame et garde la référence
            new_message = await self.ctx.send(file=discord.File(path), view=self)

            # Supprime l'ancienne frame s'il y en a une
            if self.last_message:
                try:
                    await self.last_message.delete()
                except discord.NotFound:
                    pass  # le message a peut-être déjà été supprimé

            # Met à jour la référence du dernier message
            self.last_message = new_message
        else:
            await self.ctx.send("❌ Impossible de capturer DeSmuME.")

    # --- Ligne 0 ---
    @discord.ui.button(label="A", style=discord.ButtonStyle.success, row=0)
    async def a_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_command(interaction, "A")

    @discord.ui.button(label="⬆️", style=discord.ButtonStyle.primary, row=0)
    async def up_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_command(interaction, "up")

    @discord.ui.button(label="B", style=discord.ButtonStyle.danger, row=0)
    async def b_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_command(interaction, "B")

    @discord.ui.button(label="X", style=discord.ButtonStyle.success, row=0)
    async def x_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_command(interaction, "X")

    # --- Ligne 1 ---
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.primary, row=1)
    async def left_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_command(interaction, "left")

    @discord.ui.button(label="⬇️", style=discord.ButtonStyle.primary, row=1)
    async def down_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_command(interaction, "down")

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.primary, row=1)
    async def right_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_command(interaction, "right")

    @discord.ui.button(label="Y", style=discord.ButtonStyle.success, row=1)
    async def y_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_command(interaction, "Y")

    # --- Ligne 2 (x2) ---
    @discord.ui.button(label="A x2", style=discord.ButtonStyle.success, row=2)
    async def a_double_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_command(interaction, "A", repeat=2)

    @discord.ui.button(label="⬆️ x2", style=discord.ButtonStyle.primary, row=2)
    async def up_double_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_command(interaction, "up", repeat=2)

    @discord.ui.button(label="B x2", style=discord.ButtonStyle.danger, row=2)
    async def b_double_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_command(interaction, "B", repeat=2)

    # --- Ligne 3 (x2) ---
    @discord.ui.button(label="⬅️ x2", style=discord.ButtonStyle.primary, row=3)
    async def left_double_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_command(interaction, "left", repeat=2)

    @discord.ui.button(label="⬇️ x2", style=discord.ButtonStyle.primary, row=3)
    async def down_double_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_command(interaction, "down", repeat=2)

    @discord.ui.button(label="➡️ x2", style=discord.ButtonStyle.primary, row=3)
    async def right_double_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_command(interaction, "right", repeat=2)

    @discord.ui.button(label="🔄", style=discord.ButtonStyle.secondary, row=2)
    async def capture_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)  # évite le "Thinking..."
        path = capture_desmume()
        if path:
            await interaction.followup.send(file=discord.File(path), ephemeral=False)
        else:
            await interaction.followup.send("❌ Capture échouée : DeSmuME non détecté.", ephemeral=True)


        

capture_counter = 0
def capture_desmume(output="screenshot.png"):
    global capture_counter
    time.sleep(0.3)
    try:
        win = gw.getWindowsWithTitle("DeSmuME")[0]
        if win.isMinimized or not win.visible:
            win.restore()
            

        # Coordonnées de la fenêtre
        left, top = win.left + 10, win.top + 80
        width, height = win.width - 20, win.height - 90

        region = {"left": left, "top": top, "width": width, "height": height}

        output = "screenshot.png"
        with mss.mss() as sct:
            img = sct.grab(region)
            Image.frombytes("RGB", img.size, img.rgb).save(output)

        os.makedirs("Archives", exist_ok=True)

        capture_counter += 1  # ici on modifie la variable globale
        archive_path = os.path.join("archives", f"screenshot_{capture_counter}.png")
        shutil.copy(output, archive_path)

        return output
    except IndexError:
        print("Fenêtre DeSmuME non trouvée.")
        return None

@bot.command()
async def start(ctx):
    path = capture_desmume()
    if not path:
        await ctx.send("❌ Impossible de capturer DeSmuME.")
        return

    view = PokemonControlView(ctx)
    await ctx.send("Capture du jeu :", file=discord.File(path), view=view)

@bot.command()
async def save(ctx):
    """Demande à DeSmuME de faire une save-state immédiate"""
    # On écrit le mot-clé spécial dans input.txt
    with open("input.txt", "w") as f:
        f.write("SAVE")
    await ctx.send("💾 Sauvegarde du jeu")


@bot.command()
async def capture(ctx):
    """Capture la fenêtre DeSmuME"""
    path = capture_desmume()
    if path:
        await ctx.send(file=discord.File(path))
    else:
        await ctx.send("❌ Fenêtre DeSmuME non trouvée.")


token = os.getenv('DISCORD_TOKEN')
bot.run(token)
