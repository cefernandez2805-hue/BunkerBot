import os
import threading
import discord
from flask import Flask

# Servidor web simple para que Render mantenga el puerto abierto y activo
app = Flask("")


@app.route("/")
def home():
  return "¡BunkerBot está en línea y funcionando!"


def run_web():
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)


# Configuración del bot de Discord con intents de miembros habilitados
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f"¡BunkerBot se ha conectado con éxito como {client.user}!")

  # ID del canal de información #📁┃ informacion
  INFO_CHANNEL_ID = 1557188730853531718
  channel = client.get_channel(INFO_CHANNEL_ID)

  if channel:
    embed = discord.Embed(
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
    await channel.send(embed=embed)
    print("¡Mensaje de información de roles enviado con éxito!")
  else:
    print("No se pudo encontrar el canal de información. Revisa el ID.")


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


# Iniciar el servidor web en un hilo secundario para mantener el servicio activo en Render
threading.Thread(target=run_web).start()

# Iniciar el bot usando de forma segura la variable de entorno TOKEN
client.run(os.environ["TOKEN"])
