# coding: utf-8

from flask import Flask, request
from actions import obtener_texto, enviar_mensaje, formato_texto
from dotenv import load_dotenv

# Creamos un objeto de Flask:
app = Flask(__name__)

# Ruta defecto:
@app.route("/", methods=["GET"])
def hello():
    return "Hello World :3"

# Ruta para los webhooks, en donde se recibirán y enviarán mensajes:
# Esto lo que hará será crear un url en el que nuestro bot atenderá peticiones;
# PARA RECIBIR MENSAJES:
@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    WEBHOOKTOKEN = load_dotenv("WEBHOOKTOKEN")
    
    # Si la plataforma está conectando con nuestro bot:
    if request.method == "GET":

        # Obtiene el token del formato en que lo envía META:
        if (
            request.args.get("hub.mode") == "subscribe" and
            request.args.get("hub.verify_token") == WEBHOOKTOKEN
        ):
            return request.args.get("hub.challenge")
        else:
            return "WEBHOOK TOKEN incorrecto :c", 400
    

    # Si nuestro bot está conectando a la plataforma:
    # PARA ENVIAR MENSAJES:
    elif request.method == "POST":
        try:
            # Se obtiene el número de teléfono:
            body = request.get_json()
            entry = body["entry"][0]
            changes = entry["changes"][0]
            value = changes["value"]
            message = value["messages"][0]
            number = message["from"]

            # Se recibe el mensaje y se extrae el texto:
            text = obtener_texto(message)

            # Se procesa el mensaje y se responde:
            response = respuestas_bot(text, number)
            return "Mensaje respondido :3"
        
        except Exception as error:
            return "Mensaje no enviado " + str(error) + ":c"


def respuestas_bot(text, number):
    if "hola" in text.lower():
        return enviar_mensaje(formato_texto(number, "¡Hola! ¿Cómo estás?"))
    elif "adiós" in text.lower():
        return enviar_mensaje(formato_texto(number, "¡Hasta luego!"))
    else:
        return enviar_mensaje(formato_texto(number, "Saluditos :3"))
        

# Punto de ejecución:
if __name__ == "__main__":
    app.run()