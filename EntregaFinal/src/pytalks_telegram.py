from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from src.chatbot2 import ChatterBot


TOKEN = '1021080976:AAEV3yOGT1qE1k2PlGAoFR0L5yUdTjW5gtc'
chatterBot = ChatterBot()


def start(bot, update):
    response_message = "Welcome! Are you completely new to programming? If not then we presume you will be looking" \
                       " for information about why and how to get started with Python. Fortunately an experienced" \
                       " programmer in any programming language (whatever it may be) can pick up Python very quickly." \
                       " It's also easy for beginners to use and learn, so jump in!"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def unknown(bot, update):
    response_message = "----------------"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def get_response(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=chatterBot.chatter_response(update.message.text)
    )


def main():
    updater = Updater(token=TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(
        CommandHandler('start', start)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.text, get_response)
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()