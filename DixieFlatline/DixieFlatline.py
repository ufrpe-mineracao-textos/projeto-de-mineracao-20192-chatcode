from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from chatterbotTest import ChatterBot

TOKEN = '1055571692:AAGkazHyImrWA2vPUa2j_-5UEq_ymD8G-UE'
chatterBot = ChatterBot() 

def start(bot, update):
    response_message = "____Dixie____FlatLine___-> Howdy there, cowboy!"
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
    main()
