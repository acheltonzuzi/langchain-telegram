from telegram import Update
from telegram.ext import filters,ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os


load_dotenv()

chat=ChatGroq(temperature=0, model_name="Llama3-70b-8192")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Updade {update} caused error {context.error}')

def resposta(text:str)->str:
    response=chat.invoke(text)
    return response.content

async def mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type:str=update.message.chat.type
    text:str=update.message.text

    print(f'User {update.message.chat.id} in {message_type} "{text}"')

    response:str=resposta(text)
    print('bot:',response)
    await update.message.reply_text(response)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Ola,Eu sou o assistente virtual do Kamba code, como posso te ajudar?")


if __name__=='__main__':
    print('start bot...')
    application = ApplicationBuilder().token(os.environ.get('TOKEN')).build()
    #messages
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(MessageHandler(filters.TEXT,mensagem))
    application.add_error_handler(error)

    
    print('pooling...')
    application.run_polling(pool_timeout=3)
