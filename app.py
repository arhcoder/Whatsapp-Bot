# coding: utf-8

from flask import Flask, request, jsonify
from dotenv import load_dotenv
from actions import obtener_texto, enviar_mensaje, formato_template, formato_texto
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
  
  # Palabras clave para preguntas sobre horarios:
  horario_keywords = [u"hora", u"horario", u"cuándo", u"cuando"]

  # Palabras clave para preguntas sobre el lugar:
  lugar_keywords = [u"lugar", u"localización", u"localizacion", u"dónde", u"donde"]

  # Texto de entrada:
  text = text.lower()

  # Verifica la pregunta del usuario
  if any(keyword in text for keyword in horario_keywords):
      message = "Lunes, miércoles y jueves de 3:00 a 5:00 (hora de México 🇲🇽) 😉\nTambién transmitimos las clases en vivo en Youtube:\nhttps://www.youtube.com/@ClubDeProgramacionCreativa/streams"
  elif any(keyword in text for keyword in lugar_keywords):
      message = "Laboratorio 204 de la Universidad Autónoma de Aguascalientes 🧐\nTambién transmitimos las clases en vivo en Youtube:\nhttps://www.youtube.com/@ClubDeProgramacionCreativa/streams"
  else:
      message = "*¡Bienvenido al Club de Programación Creativa!* 🐈\nSomos un grupo de apasionados por la automatización y los bots. Creamos proyectos y aprendemos programación.\nPregúntame lo que necesites y no olvides suscribirte a https://youtu.be/mLpH-yDq9Z4?si=oasYM8ZfVumKA4tm"

  # Envía el mensaje:
  return enviar_mensaje(formato_texto(number, message))

# Punto de ejecución:
if __name__ == "__main__":
    app.run()