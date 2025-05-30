from telegram.ext import (
    MessageHandler,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters
)
from telegram import (
    Update,
)
import requests
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key: str = os.getenv("api_key")
token: str = os.getenv("token")

client = genai.Client(api_key=api_key)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text="اهلاً بك في بوت توليد المحتوى التلقائي."
    )
    
    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text="يمكنك استخدام هذا البوت من خلال كتابة امر /run وكتابة عنوان المحتوى الذي ترغب في توليده."
    )
    
async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    message: str = context.args
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"اكتب مقالة احترافية عن: {message}. اجعل المقالة ذات جودة عالية وجاهزة للنشر. اكتب المقالة فقط ولا تكتب أي شيء اخر."
    )
    with open("respones.txt", "w+") as content:
        content.write(response.text)
        
    await context.bot.send_document(
        chat_id=chat_id,
        document="respones.txt"
    )
    
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    user_first_name = update.message.from_user.first_name
    responses: list[str] = ["مرحبا", "السلام عليكم", "كيف الحال"]
    
    if message == responses[0]:
        await update.message.reply_text(
            f"مرحباً بك {user_first_name}"
        )
    elif message == responses[1]:
        await update.message.reply_text(
        f"وعليكم السلام ورحمة الله وبركاته"
        )
    elif message == responses[2]:
        await update.message.reply_text(
            f"بخير شكراً لك"
        )    
    else:
        await update.message.reply_text(
            "عذراً لا افهم ماذا تقول، برجاء استخدام الاوامر."
        )
    
if __name__ == "__main__":
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("run", run))
    
    application.add_handler(MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=message_handler))
    
    application.run_polling()