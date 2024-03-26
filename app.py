# coding: utf-8

from flask import Flask, request, jsonify
from dotenv import load_dotenv
from actions import obtener_texto, enviar_mensaje, formato_template
import os

import random
import datetime

# Objeto de Flask con la aplicación:
app = Flask(__name__)

# Ruta de saludo:
@app.route("/hola", methods=["GET"])
def  bienvenido():
    return "Hola mundo :3"

# Esta ruta para webhooks con el método "GET" es el estándar de
# META para registrarlo como una API legítima:
@app.route("/webhook", methods=["GET"])
def verificar_webhook():
    try:
        # El TOKEN que nosotros inventamos para comprobar la conexión a META;
        # Además de un "challenge", que es un dato propio de META para verificación:
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        # Nuestro Token que creamos para verificar conexiones:
        load_dotenv()
        WEBHOOKTOKEN = os.getenv("WEBHOOKTOKEN")
        
        # Verificación de TOKEN:
        if token == WEBHOOKTOKEN and challenge != None:
            return challenge
        else:
            return "Conexión con META incorrecta :c", 403
    except Exception as error:
        return error, 403

# Esta ruta para webhook con método POST es para recibir mensajes
# de texto y contestar con respecto a estos:
@app.route("/webhook", methods=["POST"])
def recibir_mensajes():
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
        return jsonify({"status": "success", "message": "Mensaje respondido :3", "response": response, "from": number, "text": text})
    
    except Exception as error:
        return jsonify({"status": "error", "message": "Mensaje no enviado", "error": str(error)})

# Respuestas e interacciones de texto del bot:
def respuestas_bot(text, number):

    # Si el mensaje de texto contiene un "hola":
    if "hola" in text.lower():
        # Variables para un template llamado "saludo":
        dado1 = str(random.randint(1, 6))
        dado2 = str(random.randint(1, 6))
        
        return enviar_mensaje(formato_template("saludo", number, [dado1, dado2]))
    
    # Si el mensaje de texto contiene un "hora":
    elif "hora" in text.lower():
        # Variables para un template llamado "hora":
        fecha = datetime.datetime.now()
        hora = fecha.hour
        minutos = fecha.minute
        return enviar_mensaje(formato_template("hora", number, [hora, minutos]))
    
    # Si no coincide con saludo ni hora, envía un mensaje predeterminado:
    else:
        return enviar_mensaje(formato_template("default", number, []))

# Punto de ejecución:
if __name__ == "__main__":
    app.run()