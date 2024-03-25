# coding: utf-8

import requests
import json

from dotenv import load_dotenv

def obtener_texto(message):
    # Anaiza el formato del mensaje:
    type_message = message.get("type", None)
    if type_message == "text":
        return message["text"]["body"]
    elif type_message == "button":
        return message["button"]["text"]
    elif type_message == "interactive":
        if message["interactive"]["type"] == "list_reply":
            return message["interactive"]["list_reply"]["title"]
        elif message["interactive"]["type"] == "button_reply":
            return message["interactive"]["button_reply"]["title"]
    return "Mensaje no procesado :c"


# FUNCIÓN PARA ENVIAR MENSAJES:
def enviar_mensaje(message_json):
    # Construye un formato para enviar el mensaje construyendo el json para el request:
    TOKEN = load_dotenv("TOKEN")
    ENDPOINT = load_dotenv("ENDPOINT")

    try:
        headers = {"Content-Type": "application/json",
                   "Authorization": "Bearer " + TOKEN}
        
        response = requests.post(ENDPOINT, headers=headers, data=message_json)

        # Si se envía un error 200:
        if response.status_code == 200:
            return "Mensaje enviado :3"
        else:
            return "Mensaje no enviado :3", response.status_code
    
    except Exception as error:
        return error, 403


# CONSTRUYE UN JSON CON UN MENSAJE DE TEXTO:
def formato_texto(number, text):
    data = json.dumps({
        "messaging_product": "whatsapp",    
        "recipient_type": "individual",
        "to": number,
        "type": "text",
        "text": {"body": text}
    })
    return data