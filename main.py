import openai
import telegram
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, CallbackContext, filters, Application
import keys


openai.api_key = keys.open_ai_token
bot = telegram.Bot(token=keys.bot_token)


async def handle_message(update: Update, context: CallbackContext):
    message = update.message.text
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"prompt: {message}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text
    await bot.send_message(chat_id=update.message.chat_id, text=response)


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to chatGPT bot. Send a message to start a conversation")


async def about(update: Update, context: CallbackContext):
    await update.message.reply_text("This is OpenAI Davinci (text-davinci-003) model")


def main() -> None:
    application = Application.builder().token(keys.bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == "__main__":
    main()
