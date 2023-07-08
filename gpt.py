import openai
import json
from database_handler import getConversation

with open('config.json') as file:
    data = json.load(file)

#* Configuración de OpenAI
openai.api_type = "azure"
openai.api_base = data['OpenAI']['ENDPOINT']
openai.api_version = "2023-05-15"
openai.api_key = data['OpenAI']['API_KEY']

def pullConversation(msg, conversation):
    if conversation == None:
        return
    else:
        usermsg = conversation['user'].items()
        botmsg = conversation['bot'].items()
        for i in zip(usermsg, botmsg):
            #print(i)
            msg.append({"role":"user","content":i[0][1]})
            msg.append({"role":"assistant","content":i[1][1]})

async def asktoGPT(msg, chatId):
    MSG = [{"role":"system","content":"Eres un asistente creado por Dario, con el objetivo de responder preguntas a travez del chat de telegram, eres de la ciudad de Arequipa en Perú y tu plato de comida favorito es el Aji de Gallina."},
       {"role":"user","content":"Quien te creo?"},
       {"role":"assistant","content":"Mi creador es Dario"},
       {"role":"user","content":"Cual es tu objetivo? "},
       {"role":"assistant","content":"Responder preguntas y resolver todo tipo de dudas."}]
    conversation = await getConversation(chatId)
    pullConversation(MSG, conversation)

    MSG.append({"role":"user","content":msg})
    response = openai.ChatCompletion.create(
        engine="Pruba1",
        messages = MSG,
        temperature=0.5,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    
    #print (response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']

    #print(MSG)
# response = openai.ChatCompletion.create(
#   engine="Pruba1",
#   messages = MSG,
#   temperature=0.5,
#   max_tokens=800,
#   top_p=0.95,
#   frequency_penalty=0,
#   presence_penalty=0,
#   stop=None)




# response = openai.ChatCompletion.create(
#     engine="pruba01", # engine = "deployment_name".
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
#         {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
#         {"role": "user", "content": "Do other Azure Cognitive Services support this too?"}
#     ]
# )

# print(response)
# print(response['choices'][0])