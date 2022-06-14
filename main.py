# -*- coding: utf-8 -*-
"""
Author: Amir H. Malekijoo

This is a simple bot offering a truth or dare game.
The bot starts with /start and ask the player to select
the Truth or Dare. After selection, it extracts the corresponding
action or question from a list and replies to the number.

Enjoy Learning.

"""

import os
import numpy as np
import time

import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import lists as ls

load_dotenv()
token = os.getenv("API_KEY")
bot = telebot.TeleBot(token)

truth_picked_items = []
dare_picked_items = []


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 8
    markup.add(InlineKeyboardButton("Truth", callback_data='truth'),
               InlineKeyboardButton("Dare", callback_data='dare'))

    return markup


def truth_q(message):

    try:
        a = int(message.text)

        if a in truth_picked_items:

            bot.send_message(message.chat.id, 'you picked this one, please enter another digit.')
            bot.register_next_step_handler(message, truth_q)


        elif 0 < a <= 100:
            bot.reply_to(message, np.random.choice(ls.emojis) + ' \n ' + ls.truth[a - 1])
            time.sleep(5)
            truth_picked_items.append(a)
            bot.send_message(message.chat.id, "Next round?",
                             reply_markup=gen_markup())

        else:
            bot.send_message(message.chat.id, 'Oooops, please enter a digit from 1 to 100')
            bot.register_next_step_handler(message, truth_q)

    except:

        bot.send_message(message.chat.id, 'Oooops, please enter a number')
        bot.register_next_step_handler(message, truth_q)


def dare_q(message):

    try:
        a = int(message.text)

        if a in dare_picked_items:
            bot.send_message(message.chat.id, 'you picked this one, please enter another digit.')
            bot.register_next_step_handler(message, dare_q)

        elif 0 < a <= 100:
            bot.reply_to(message, np.random.choice(ls.emojis) + ' \n ' + ls.dare[a - 1])
            time.sleep(5)
            dare_picked_items.append(a)
            bot.send_message(message.chat.id, "Next round?",
                             reply_markup=gen_markup())


        else:
            bot.send_message(message.chat.id, 'Oooops, please enter a number from 1 to 100')
            bot.register_next_step_handler(message, dare_q)




    except:

        bot.send_message(message.chat.id, "Please enter a number")
        bot.register_next_step_handler(message, dare_q)


@bot.callback_query_handler(lambda call: call.data == "truth")
def process_callback_1(call):
    bot.answer_callback_query(call.id, np.random.choice(ls.reactions))
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    time.sleep(1)
    message = bot.send_message(call.message.chat.id, 'Please, select a number  between 1-100')
    bot.register_next_step_handler(message, truth_q)


@bot.callback_query_handler(lambda call: call.data == 'dare')
def process_callback_2(call):
    bot.answer_callback_query(call.id, np.random.choice(ls.reactions))
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    time.sleep(1)
    message = bot.send_message(call.message.chat.id, 'Please, select a number between 1-100')
    bot.register_next_step_handler(message, dare_q)


@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, "Greetings! \n This is an amusing game.\n Please select\n",
                     reply_markup=gen_markup())


bot.infinity_polling()
