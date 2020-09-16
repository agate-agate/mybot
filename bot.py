import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
import easy_planets

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


def tell_user_about_planet(update, context):
    print('Вызван /planet')

    print('update:')
    print(update)
    print('context:')
    print(context)
    print('update.message.text:')
    print(update.message.text)

    user_text = str(update.message.text)
    text_pieces = user_text.split()

    try:
        raw_planet_name = str(text_pieces[1])
    except IndexError:
        raw_planet_name = ''

    planet_name = easy_planets.normalize_planet_name(raw_planet_name)

    ephem_planet = easy_planets.get_ephem_planet(planet_name)

    constellation_label = easy_planets.get_constellation_label_for_planet(ephem_planet)

    message_lines = [
        'Вызван /planet',
        f'Ты хочешь узнать про планету: {raw_planet_name}',
        f'Которая распозналась как: {planet_name}',
        f'Она находится в созвездии: {constellation_label}',
    ]
    update.message.reply_text('\n'.join(message_lines))


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
    dp.add_handler(CommandHandler('planet', tell_user_about_planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
