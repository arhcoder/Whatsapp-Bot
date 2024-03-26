# coding: utf-8

import requests
from dotenv import load_dotenv
import json
import os

# Anaiza el formato del mensaje:
def obtener_texto(message):
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
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    ENDPOINT = os.getenv("ENDPOINT")
    print(message_json)

    try:
        headers = {"Content-Type": "application/json",
                   "Authorization": "Bearer " + TOKEN}
        response = requests.post(ENDPOINT, headers=headers, data=message_json)
        print(response.status_code)
        print(response.content)

        # Si se envía un error 200:
        if response.status_code == 200:
            return "Mensaje enviado :3"
        else:
            return "Mensaje no enviado :3", response.status_code
    
    except Exception as error:
        return error, 403


# CONSTRUYE UN JSON CON UN MENSAJE DE TEXTO TEMPLATE:
def formato_texto(number, text):
    message = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return message


# CONSTRUYE UN JSON CON UN MENSAJE DE TEXTO:
def formato_template(template_name, number, variables):
    parameters = [{"type": "TEXT", "text": variable} for variable in variables]
    message = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": "es_MX"},
            "components": [
                {
                    "type": "BODY",
                    "parameters": parameters
                }
            ]
        }
    }
    return json.dumps(message)