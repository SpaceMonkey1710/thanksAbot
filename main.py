import telebot
import os
import random
from datetime import datetime

import constants
import lyrics


TOKEN = constants.TOKEN
LYRICS = lyrics.LYRICS
bot = telebot.TeleBot(TOKEN)


print(bot.get_me())


def log(message, answer):
    print('\n------')
    print(datetime.now())
    print('Message from: {0} {1}. (id = {2}) \n Text: {3}'.format(message.from_user.first_name,
                                                                  message.from_user.last_name,
                                                                  str(message.from_user.id),
                                                                  message.text))
    print(answer)


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Random \U0001F3B2 song')
    bot.send_message(message.from_user.id,
                     'Welcome, ' + message.from_user.first_name +
                     '!\nPress \U0001F3B2 button, to get a random song!',
                     reply_markup=user_markup)


@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id,
                     '''Press \U0001F3B2 button to get a random song.\n''' +
                     '''Sometimes it takes extra wait time, so be patient \u270C\uFE0F''')


@bot.message_handler(commands=['stop'])
def handle_stop(message):
    hide_markup = telebot.types.ReplyKeyboardMarkup()
    bot.send_message(message.from_user.id, 'Okay... Come back soon!', reply_markup=hide_markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    print(message)
    answer = 'Something went wrong. Please, press /help.'

    if message.text == 'Random \U0001F3B2 song':
        bot.send_message(message.chat.id, '''Picking a song for you...''')
        with open('songs.txt') as f:
            songs = f.readlines()
            song = random.choice(songs)
            file = 'https://lk.selectyre.ru/songs/' + str(song)
            audio = file
            bot.send_chat_action(message.from_user.id, 'upload_audio')
            bot.send_audio(message.from_user.id, audio)
            bot.send_message(message.chat.id, lyrics.LYRICS[file.rstrip('\n)')])

    else:
        bot.send_message(message.chat.id, answer)

        log(message, answer)


bot.polling(none_stop=True, interval=0)