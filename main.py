import asyncio
import os
import threading
import discord
from flask import Flask

# Servidor web simple para mantener el servicio activo en Render
app = Flask("")


@app.route("/")
def home():
  return "¡BunkerBot está en línea y funcionando!"


def run_web():
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)


# Configuración del bot con intents habilitados (incluyendo reacciones y miembros)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents)

# Diccionario que conecta cada emoji de bandera con el nombre del país
COUNTRY_ROLES = {
    "🇨🇴": "Colombia",
    "🇲🇽": "México",
    "🇪🇸": "España",
    "🇻🇪": "Venezuela",
    "🇵🇷": "Puerto Rico",
    "🇪🇨": "Ecuador",
    "🇦🇷": "Argentina",
    "🇨🇱": "Chile",
    "🇧🇴": "Bolivia",
    "🇬🇹": "Guatemala",
    "🇸🇻": "El Salvador",
    "🇭🇳": "Honduras",
    "🇳🇮": "Nicaragua",
    "🇨🇷": "Costa Rica",
    "🇵🇦": "Panamá",
    "🇨🇺": "Cuba",
    "🇩🇴": "República Dominicana",
    "🇵🇪": "Perú",
    "🇵🇾": "Paraguay",
    "🇺🇾": "Uruguay",
}

AUTOROLE_CHANNEL_ID = 1557197785684508733


@client.event
async def on_ready():
  print(f"¡BunkerBot se ha conectado con éxito como {client.user}!")

  # 1. Canal de información de roles
  INFO_CHANNEL_ID = 1557188730853531718
  info_channel = client.get_channel(INFO_CHANNEL_ID)

  if info_channel:
    messages = [m async for m in info_channel.history(limit=5)]
    if not any(
        m.author == client.user and "Información de Roles" in str(m.embeds)
        for m in messages
    ):
      embed_info = discord.Embed(
          title="🛡️┃ Información de Roles",
          description="""**Roles de Nivel**
En este apartado podrás encontrar la información de los roles del servidor que se te otorgan mediante vas subiendo de nivel (siendo activo en el chat), junto a los beneficios que estos llevan. Si tienes alguna duda extra puedes abrir un ticket en el canal de <#1557200977457709129>
El bot de nivelación que se utiliza es <@437808476106784770>, el prefijo que se utiliza es /, para poder ver tu nivel solo usa /rank en el canal de <#1557199769854812240>

🔹 **Nivel 10**
> ・Podrás enviar imágenes por <#1557199455537729546>

🔹 **Nivel 100**
> ・Tendrás acceso a un canal de texto y voz privados (VIP)

**Booster**
Beneficios que adquieres al boostear el servidor, reclámalos en <#1557200977457709129>
> ・Color personalizados VIP o normal.
> ・Canal de texto y voz privado.
> ・Enviar multimedia por todos los canales del servidor.
> ・Subir 5 niveles en el servidor.
> ・Participar en <#1557566930511073380>""",
          color=0xFFB300,
      )
      await info_channel.send(embed=embed_info)
      print("¡Mensaje de información de roles enviado!")

  # 2. Canal de Autoroles (con el emoji 🍁 y las reacciones de banderas automáticas)
  autorole_channel = client.get_channel(AUTOROLE_CHANNEL_ID)

  if autorole_channel:
    messages = [m async for m in autorole_channel.history(limit=5)]
    autorole_msg = None
    for m in messages:
      if m.author == client.user and m.embeds and "ELIGE TU PAÍS" in m.embeds[0].title:
        autorole_msg = m
        break

    if not autorole_msg:
      embed_autoroles = discord.Embed(
          title="🦝 │ ¡ELIGE TU PAÍS!",
          description=(
              "🍁 │ **REACCIONA A ESTE MENSAJE CON LA BANDERA DE TU PAÍS**\n\n"
              "1. Solo se puede seleccionar un país.\n"
              "2. Si te equivocas y tienes que cambiar de país; primero **quita"
              " la reacción** y luego vuelve a reaccionar al país que deseas.\n"
              "3. Evita usar todos los emojis y así evitas bugs. Y listo,"
              " **disfruta del server con tu nuevo rol!** 🧑‍💻"
          ),
          color=0xFFB300,
      )
      embed_autoroles.set_footer(
          text=(
              "En caso tengas dudas o reportes con algún bug, no dudes en abrir"
              " un ticket."
          )
      )

      autorole_msg = await autorole_channel.send(embed=embed_autoroles)
      print("¡Mensaje de autoroles enviado con éxito!")

      # Añadir automáticamente todas las reacciones de las banderas
      for emoji in COUNTRY_ROLES.keys():
        try:
          await autorole_msg.add_reaction(emoji)
          await asyncio.sleep(0.4)
        except Exception as e:
          print(f"No se pudo añadir la reacción {emoji}: {e}")


# Evento cuando un usuario añade una reacción para obtener su rol de país
@client.event
async def on_raw_reaction_add(payload):
  if payload.channel_id != AUTOROLE_CHANNEL_ID:
    return
  if payload.user_id == client.user.id:
    return

  emoji_str = str(payload.emoji)
  if emoji_str in COUNTRY_ROLES:
    country_name = COUNTRY_ROLES[emoji_str]
    guild = client.get_guild(payload.guild_id)
    if guild:
      member = guild.get_member(payload.user_id)
      if not member:
        try:
          member = await guild.fetch_member(payload.user_id)
        except Exception as e:
          print(f"No se pudo obtener el miembro: {e}")
          return

      if member.bot:
        return

      # Busca el rol probando el formato con barra | , sin barra, o solo el nombre
      role = (
          discord.utils.get(guild.roles, name=f"{emoji_str} | {country_name}")
          or discord.utils.get(guild.roles, name=f"{emoji_str} {country_name}")
          or discord.utils.get(guild.roles, name=country_name)
      )

      if role:
        try:
          await member.add_roles(role)
          print(f"¡Rol {role.name} asignado a {member.name}!")
        except Exception as e:
          print(
              f"Error al asignar el rol (asegúrate de que el rol del bot esté"
              f" arriba de los países y tenga permisos de Administrador o"
              f" Gestionar roles): {e}"
          )
      else:
        print(f"No se encontró el rol para {country_name}")


# Evento cuando un usuario quita su reacción para quitarle el rol
@client.event
async def on_raw_reaction_remove(payload):
  if payload.channel_id != AUTOROLE_CHANNEL_ID:
    return
  if payload.user_id == client.user.id:
    return

  emoji_str = str(payload.emoji)
  if emoji_str in COUNTRY_ROLES:
    country_name = COUNTRY_ROLES[emoji_str]
    guild = client.get_guild(payload.guild_id)
    if guild:
      member = guild.get_member(payload.user_id)
      if not member:
        try:
          member = await guild.fetch_member(payload.user_id)
        except Exception as e:
          print(f"No se pudo obtener el miembro: {e}")
          return

      if member.bot:
        return

      role = (
          discord.utils.get(guild.roles, name=f"{emoji_str} | {country_name}")
          or discord.utils.get(guild.roles, name=f"{emoji_str} {country_name}")
          or discord.utils.get(guild.roles, name=country_name)
      )

      if role:
        try:
          await member.remove_roles(role)
          print(f"¡Rol {role.name} removido de {member.name}!")
        except Exception as e:
          print(f"Error al remover el rol: {e}")


# Evento automático cuando banean a un usuario
@client.event
async def on_member_ban(guild, user):
  BAN_CHANNEL_ID = 1557188976916307968
  channel = guild.get_channel(BAN_CHANNEL_ID)

  if not channel:
    try:
      channel = await client.fetch_channel(BAN_CHANNEL_ID)
    except Exception as e:
      print(f"No se pudo obtener el canal de baneo: {e}")
      return

  if channel:
    created_timestamp = int(user.created_at.timestamp())

    embed = discord.Embed(
        title="🚫 Usuario Baneado",
        description=f"**{user.name}** ha sido baneado del servidor",
        color=0xFF0000,
    )
    embed.add_field(
        name="👤 Usuario", value=f"<@{user.id}>\n{user.name}", inline=False
    )
    embed.add_field(name="🆔 ID", value=f"`{user.id}`", inline=False)
    embed.add_field(
        name="📅 Cuenta creada", value=f"<t:{created_timestamp}:R>", inline=False
    )
    embed.add_field(
        name="📜 Recordatorio",
        value="Recuerda leer las reglas del servidor en <#1557187229133181060>",
        inline=False,
    )

    if user.avatar:
      embed.set_thumbnail(url=user.avatar.url)

    await channel.send(embed=embed)
    print(f"¡Alerta de baneo enviada para {user.name}!")


# Iniciar el servidor web en un hilo secundario
threading.Thread(target=run_web).start()

# Iniciar el bot de Discord
client.run(os.environ["TOKEN"])
