from database_handler import sendToDatabase, clearDatabase
from typing import Final
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, filters, ContextTypes, Application
from gpt import asktoGPT
import json

#Leer json
with open('config.json') as file:
    data = json.load(file)

#* Configuración de Telegram
#? Este es el token del bot de prueba y su alias es @tester3005bot
TOKEN: Final = data['Telegram']['TOKEN']
BOT_USERNAME: Final = data['Telegram']['BOT_NAME']

#* COMANDOS: /start, /help, /custom
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hola! soy un bot de prueba')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('No hay nada que pueda ayudarte')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Este es un comando personalizado, puedes agregarlo con /custom')

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await clearDatabase(update.message.chat_id)
    await update.message.reply_text('El contexto ha sido limpiado, el bot ya no recuerda nada de lo que hablaron.')

#* RESPUESTAS
async def handle_response(text):
    processed_text = text.lower()
    if 'hola' in processed_text:
        return 'Hola, humano!'
    if 'adios' in processed_text:
        return 'Adios, humano!'
    return 'No entiendo lo que dices, humano'

# async def handle_responseAI(text: str) -> str:
#     processed_text = text.lower()
#     response = openai.ChatCompletion.create(
#         engine="pruba1", # engine = "deployment_name".
#         messages=[
#             {"role": "system", "content": "Eres un bot creado por Dario."},
#             {"role": "user", "content": processed_text}
#         ]
#     )
#     return response['choices'][0]['message']['content']

#! 1: Mando a openAI el mensaje del usuario junto con los demas mensajes de la conversación
#! 2: si se mando el mensaje a openAI, se guarda en la base de datos tanto el mensaje como la respuesta
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    user = update.message.from_user
    
    #* Enviar mensaje a la base de datos

    print(f'User ({update.message.chat.id}) sent a message: {text}')
    
    try:
        #TODO: Enviar mensaje a OpenAI junto con los demas mensajes de la conversación
        response = await asktoGPT(text, update.message.chat.id)        
        await update.message.reply_text(response)

        #* Enviar respuesta a la base de datos solo si funciono
        await sendToDatabase(text, update.message.chat.id, 'user')
        await sendToDatabase(response, update.message.chat.id, 'bot')
    except Exception as error:
        print(f'Error: {error}')
        response: str = "Error: %s" % error
        await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot')
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('clear', clear_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # app.add_handler(MessageHandler(filters.LOCATION, handle_Location))

    app.add_error_handler(error)

    print('Bot started')
    app.run_polling(poll_interval=3)
