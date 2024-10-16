import os
from dotenv import load_dotenv
from typing import Final
from telegram import  Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from gqrcode import generate_qr
load_dotenv()


TOKEN=os.getenv("TOKEN")
BOT_USERNAME: Final="@YourQrCode_Bot"


# commands
async def start_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("**Hello** 👋\n Send url or text to generate QR code")

async def help_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Just send text or url to generate QR code")

async def custom_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("sorry, this command is not available yet")


# responses

def handle_responce(text:str)->str:
    qr_url=generate_qr(text)
    return f"{qr_url}"

async def handle_sms(update:Update, context: ContextTypes.DEFAULT_TYPE):
    message_type:str=update.message.chat.type
    entered_text=update.message.text
    user=update.message.chat.id
    print(f"user: {user}, in message type: {message_type}, text: {entered_text}")

    if message_type=="group":
        if BOT_USERNAME in entered_text:
            new_text:str=entered_text.replace(BOT_USERNAME,"").strip()
            qrcode_path:str=handle_responce(new_text)
        else:
            return
    else:
        qrcode_path:str=handle_responce(entered_text)
    print(f"Bot: {qrcode_path}")

    #send image
    try:
        with open(qrcode_path,'rb') as qr_img:
            await update.message.reply_photo(photo=qr_img,caption=f"Your Qr code✅")
    except Exception as error:
        print(f"Error occurred: {error}")
        await update.message.reply_text("Sorry😔\n I couldn't generate the QR code. Please try again later!")

async def error(update:Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Updates caused error:{context.error}")

if __name__=='__main__':
    print("Starting........")
    #build
    app=Application.builder().token(TOKEN).build()

    #command
    app.add_handler(CommandHandler("start",start_command))
    app.add_handler(CommandHandler("help",help_command))
    app.add_handler(CommandHandler("custom",custom_command))

    #messages
    app.add_handler(MessageHandler(filters.TEXT,handle_sms))

    #error
    app.add_error_handler(error)

    #polling
    print("Polling........")
    app.run_polling(poll_interval=3)