from fileinput import filename
from secrets import choice
from typing import Literal
from urllib import request, response
from discord.ext import commands, tasks
from discord import app_commands
import discord
from tools.embedtools import embed_builder
import config
from PIL import Image, ImageDraw, ImageFont
import os
import requests
from io import BytesIO
import datetime
import random



class Passport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def generate_passport(self, interaction, sukunimi, etunimi, lisanimet, kotikaupunki,sukupuoli):
        try:
            img = Image.open(f"{os.getcwd()}/anusribale/passport_template.png")
        except Exception as e:
            print(e)
        datenow = datetime.datetime.today()
        surname = sukunimi.upper()
        name = etunimi.upper()
        middlename = lisanimet.upper()
        place_of_birth = kotikaupunki.upper()
        gender = sukupuoli.upper()
        countrycode = "BUH"
        passtype = "P"
        passcode = countrycode+str(random.randint(1,10000))
        bornat = interaction.user.created_at.strftime(("%d.%m.%Y"))
        expires = datetime.date(datenow.year + 5, datenow.month, datenow.day)
        usercode = str(interaction.user.id)
        draw = ImageDraw.Draw(img)
        request = requests.get(interaction.user.avatar)
        passpic = Image.open(BytesIO(request.content)).resize((386,507))
        img.paste(passpic, (31,198))
        font = ImageFont.truetype(f"{os.getcwd()}/anusribale/Roboto-Regular.ttf", 25)

        draw.text((280, 125), passtype, (0,0,0,255), font=font)
        draw.text((575, 125), countrycode, (0,0,0,255), font=font)
        draw.text((886, 125), passcode, (0,0,0,255), font=font)

        draw.text((485, 260), surname, (0,0,0,255), font=font)
        draw.text((485, 335), name + " " + middlename, (0,0,0,255), font=font)
        draw.text((485, 405), countrycode, (0,0,0,255), font=font)
        draw.text((485, 475), bornat, (0,0,0,255), font=font)
        draw.text((485, 550), place_of_birth, (0,0,0,255), font=font)
        draw.text((485, 620), datenow.strftime(("%d.%m.%Y")), (0,0,0,255), font=font)
        draw.text((485, 690), expires.strftime(("%d.%m.%Y")), (0,0,0,255), font=font)

        draw.text((888, 330), gender, (0,0,0,255), font=font)
        draw.text((888, 405), usercode, (0,0,0,255), font=font)
        draw.text((888, 477), "BUHISTANIN POLIISI\n\nBUHISTANI POLICE", (0,0,0,255), font=font)

        draw.text((470, 783), f"{passtype}<{countrycode}<{surname}<{name}<{middlename}", (0,0,0,255), font=font)
        draw.text((470, 818), f"{passcode}<{gender}<{usercode}", (0,0,0,255), font=font)
        img.save(f"passports/{interaction.user.id}.png")
        return "done"


    city_names = [
        "Buhicity",
        "Buhinsuu",
        "Buhinmäki",
        "Buhinen",
        "Buhinpää",
        "Buhinlinna",
        "Buhkkeli",
        "Buhpio",
        "Buhinkylä",
        "Buhinkaupunki",
        "Buhinniemi",
        "Buhtaa",
        "Buhkaus",
        "Buhinranta",
        "Buhikoski",
        "Buhinkorva",
        "Buhinharju",
        "Buhinjärvi",
        "Buhinjoki",
        "Buhinniemi",
    ]

    @app_commands.command(name="passihakemus", description="Generoi sinulle passin ja nimen perusteella serverille nicknamen, lue kaikki kohdat huolellisesti.")
    @app_commands.describe(sukunimi = "Sukunimesi Buhistaniin (Älä käytä oikeaa sukunimeäsi:D). Sukunimen maksimipituus 15 kirjainta")
    @app_commands.describe(etunimi = "Etunimesi Buhistaniin. Etunimen maksimipituus 15 kirjainta")
    @app_commands.describe(lisanimet = "Mahdolliset lisanimet Buhistaniin. Tunnetaan myös nimellä toinen ja kolmas nimi. Maksimipituus 15 kirjainta")
    async def passihakemus(
    self,
    interaction:discord.Interaction,
    sukunimi: str,
    etunimi: str,
    lisanimet: str,
    kotikaupunki: Literal[
        "Buhicity",
        "Buhinsuu",
        "Buhinmäki",
        "Buhinen",
        "Buhinpää",
        "Buhinlinna",
        "Buhkkeli",
        "Buhpio",
        "Buhinkylä",
        "Buhinkaupunki",
        "Buhinniemi",
        "Buhtaa",
        "Buhkaus",
        "Buhinranta",
        "Buhikoski",
        "Buhinkorva",
        "Buhinharju",
        "Buhinjärvi",
        "Buhinjoki",
        "Buhinniemi",
    ],
    sukupuoli: Literal["Mies", "Nainen", "Taisteluhelikopteri"]
    ):
        if len(sukunimi) > 16 or len(etunimi) > 16 or len(lisanimet) > 16 or len(sukunimi) < 3 or len(etunimi) < 3 or len(lisanimet) < 3:
            await interaction.response.send_message("Liian pitkä/lyhyt etu tai sukunimi, ei mahdu passiin:D")
        elif not sukunimi.isalpha() or not etunimi.isalpha():
            await interaction.response.send_message("Nimessä voi olla ainoastaan kirjaimia")
        else:
            passport = await self.generate_passport(interaction, sukunimi, etunimi, lisanimet, kotikaupunki,sukupuoli)
            try:
                await interaction.response.send_message("Generoidaan passia, tässä saattaa kestää heti", ephemeral=True)
                file = discord.File(f"./passports/{interaction.user.id}.png")
                print(file)
                await interaction.channel.send("Paska botti vittu", file=file)
            except Exception as err:
                print(err)
    
    
    #, file = discord.File(f"{os.getcwd()}/passports/{interaction.user.id}.png")
    #await interaction.channel.send("Generoidaan passia, tässä saattaa kestää heti", ephemeral=True)
    #vittu ihan kohta menee moti tähän paskaan




async def setup(bot):
    await bot.add_cog(Passport(bot),
    guilds= [discord.Object(config.TEST_GUILD)])