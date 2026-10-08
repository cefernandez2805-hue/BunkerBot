import os
import threading
import discord
from flask import Flask

# Servidor web simple para que Render mantenga el servicio activo
app = Flask("")


@app.route("/")
def home():
  return "¡BunkerBot está en línea y funcionando!"


def run_web():
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)


# Configuración del bot de Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f"¡BunkerBot se ha conectado con éxito como {client.user}!")

  # Canal de reglas configurado
  CHANNEL_ID = 1557187229133181060

  channel = client.get_channel(CHANNEL_ID)

  if channel:
    embed = discord.Embed(
        title="REGLAS DE EL BUNKER",
        description="""<:diamanteamarillo:1302798773478494238> - Información Básica
> Es importante hacer énfasis que el servidor cuenta con un ambiente y humor bastante característico de nuestra comunidad en El Bunker, por lo tanto el staff del servidor aplica sanciones de acuerdo a una evaluación y contexto de cualquier situación particular.
> 
<:diamanteamarillo:1302798773478494238> - Respeto
> ・El servidor cuenta con una forma de ser y humor que puede rozar la falta de respeto, sin embargo, una falta de respeto no consensuada, cualquier tipo de amenaza, acoso, toxicidad, difamación, discriminación de cualquier tipo entre otros hacia un usuario no está permitido y se sancionará de manera correspondiente.
> ・No esta permitido acosar a nadie usando la foto de perfil o enviando fotos privadas de los usuarios, en caso de hacerlo se procederá con una sanción respectiva.
> 
<:diamanteamarillo:1302798773478494238> - Spam/Flood/Scam
> ・No se permite ningún tipo de Spam/Flood/Scam en el servidor.
> ・Se considera Spam cualquier tipo de promoción ya sea de una red social o link para la promoción del mismo que no este relacionado con el servidor, también aplica si se le hace por MD a un usuario.
> ・Se considera Flood la repetición de más de 5 veces un mensaje en el servidor, ya sea un emote o texto.
> ・Se considera Scam cualquier tipo de estafa (Esta da una sanción permanente sin posibilidad de apelación)
> 
<:diamanteamarillo:1302798773478494238> - Contenido NSFW +18
> ・Esta totalmente prohibido enviar cualquier tipo de contenido multimedia de carácter NSFW +18, obsceno o gore, en caso de hacerlo será baneo permanente sin posibilidad de apelación. También aplica ponerse de perfil fotos de este mismo carácter.
> 
<:diamanteamarillo:1302798773478494238> - Roles
> ・No esta permitido exigir roles o rangos en el servidor, para ser staff se avisará previamente mediante 📢 ┃ anuncios si se abren las postulaciones. Todos los roles y rangos del servidor cumplen una función pre-establecida, es importante respetar cada uno de los permisos.
> 
<:diamanteamarillo:1302798773478494238> - Staff
> ・ Es importante respetar al staff del servidor, no solo porque son los que mantienen la sana convivencia en el mismo, sino porque son los que tienen la autoridad y hacen que la comunidad cada vez crezca más.
> 
<:diamanteamarillo:1302798773478494238> - Identidad
> ・ Cualquier tipo de suplantación de Identidad ya sea de broma o no resultará en baneo permanente del servidor.
> ・Se entiende como suplantación en nuestro servidor el uso de multicuentas y aún más si son usadas para evadir sanciones.
> ・También esta prohibido hacerse pasar por otro genero, independiente si la situación es de carácter humorística o no.
> 
<:diamanteamarillo:1302798773478494238> - Menciones/Tags
> ・Prohibido hacer mención o tag de cualquier miembro del staff sin autorización. Los únicos usuarios que tienen la potestad de hacerlo son los moderadores y administradores del servidor.
> 
<:diamanteamarillo:1302798773478494238> - Bots
> ・No utilizar de manera incorrecta los bots del servidor, cada uno cumple con una función, y algunos tienen su propio canal de uso.
> 
<:diamanteamarillo:1302798773478494238> - Transmisiones y Eventos
> ・Durante las transmisiones en vivo de partidos de fútbol, UFC, boxeo, básquetbol o películas en El Estadio, se prohíbe el spam masivo y la toxicidad excesiva que arruine la experiencia de los demás.
> ・Queda estrictamente prohibido compartir enlaces maliciosos o retransmitir contenido ilegal no autorizado en los canales de voz o de escenario.
> ・Mantener el orden en la Pantalla Gigante y respetar turnos cuando se habilite la participación de la comunidad.""",
        color=0xFFB300,
    )
    await channel.send(embed=embed)
    print("¡Mensaje de reglas enviado con éxito!")
  else:
    print("No se pudo encontrar el canal. Revisa el ID.")


# Iniciar el servidor web en un hilo secundario para Render
threading.Thread(target=run_web).start()

# Iniciar el bot usando de forma segura la variable de entorno TOKEN
client.run(os.environ["TOKEN"])

