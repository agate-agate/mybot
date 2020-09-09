import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {
    'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD,
    }
}

def greet_user(update, context):
    print('Вызван /start')
    # print('update:')
    # print(update)
    # print('context:')
    # print(context)
    update.message.reply_text(
        'Привет человек! Я слышу что ты вызвал программу /start!'
    )

def talk_to_me(update, context):
    print('Вызван talk_to_me')
    # print('update:')
    # print(update)
    # print('context:')
    # print(context)
    text = str(update.message.text)
    print(text)
    update.message.reply_text('Вы присылали текст: ' + text)

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()
