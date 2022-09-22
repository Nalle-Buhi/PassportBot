import discord
import datetime

# embed handling


async def embed_builder(
    interaction, title, description, fields=None, image=None, thumbnail=None
):
    em = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.random(),
        timestamp=discord.utils.utcnow(),
    )
    em.set_author(name=interaction.user, icon_url=interaction.user.avatar)
    em.set_footer(
        text="V1.0 Beta",
        icon_url="https://raw.githubusercontent.com/Nalle-Buhi/Buhi.py/main/images/avatar.png",
    )
    """Fields takes a list in form of:
    [[name, value, inline True/False], [name2, value2, inline True/False]]"""
    if fields != None:
        for field in fields:
            fieldname, value, inline = field
            em.add_field(name=fieldname, value=value, inline=inline)
    if image != None:
        em.set_image(url=image)
    if thumbnail != None:
        em.set_thumbnail(url=thumbnail)
    return em