from firebase import firebase
import json

with open('config.json') as file:
    data = json.load(file)

#* Congiguración de Firebase
firebase = firebase.FirebaseApplication(data['Firebase']['ENDPOINT'], None)

async def clearDatabase(chatId):
    route = "/chats/%s" % chatId
    firebase.delete(route, None)

async def getConversation(chatId):
    route = "/chats/%s" % chatId
    # convertir a json la respuesta de firebase
    return firebase.get(route, None)

async def sendToDatabase(msg, chatId, sender):
    route = "/chats/%s/%s" % (chatId, sender)
    firebase.post(route, msg)
    print("Mensaje enviado a la base de datos")