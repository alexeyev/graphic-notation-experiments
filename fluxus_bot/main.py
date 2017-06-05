# -*- coding: utf-8 -*-

import configparser
import telebot
import random

from fluxus_bot.markovchain import *
from fluxus_bot.markovchain import char_level, word_level
from fluxus_bot.markovchain.char_level import MarkovianCharLevelGenerator
from fluxus_bot.markovchain.word_level import MarkovianWordLevelGenerator

config_parser = configparser.ConfigParser()
config_parser.read("configs/bot.ini")
token = config_parser.get("Credentials", "ApiToken")
bot = telebot.TeleBot(token)

scores = [line.replace("<n>", "\n").replace("[S]", "").replace("[E]", "") for line in open("parsed_texts.txt")]

print("Bot started.")


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.send_message(
        message.chat.id,
        "<b>Я — FLUXUS-бот, добрый день.</b><br><br>Доступные команды:<br>"
        " /random <br>— случайный перформанс из книги<br>"
        " /markov <char/word> <depth> <br>— сгенерированный марковской цепью перформанс<br>"
        "<br>Примеры:"
        "<br>&nbsp;&nbsp;/markov char 8"
        "<br>&nbsp;&nbsp;/markov word 2"
        "<br>&nbsp;&nbsp;/random"
        "<br><br>Чем больше \"глубина\" цепи, тем осмысленнее получится текст, "
        "но тем больше шансы, что он полностью скопирован цепью из книжки.<br><br>"
        "Бот разработан в рамках подготовки к перформансу в&nbsp;Санкт-Петербургском&nbsp;Музее&nbsp;звука:<br><br>"
        "24 июня 2017, 20:00<br>FLUXUS СПб: программа звуковых перформансов<br><br>"
        "Приходите!", parse_mode="HTML")
    print("Response:", msg)


@bot.message_handler(commands=['random'])
def send_random(message):
    try:
        random_score = scores[random.randint(0, len(scores))]
        msg = bot.send_message(message.chat.id, random_score)
        print(msg)
    except Exception as e:
        msg = bot.send_message(message.chat.id, "Oops, error " + str(e))
        print(msg)
        print(e)


@bot.message_handler(regexp="/markov char \d+")
def send_markov_char(message):
    try:
        numbers = [int(s) for s in message.text.split() if s.isdigit()]
        # todo: pretrain a lot of models
        char_generator = MarkovianCharLevelGenerator(numbers[0]).fit(char_level.TEXTS)
        generated_text = char_generator.generate_text()
        msg = bot.send_message(message.chat.id, generated_text)
        print(msg)
    except Exception as e:
        msg = bot.send_message(message.chat.id, "Oops, error " + str(e))
        print(msg)
        print(e)


@bot.message_handler(regexp="/markov word \d+")
def send_markov_char(message):
    try:
        numbers = [int(s) for s in message.text.split() if s.isdigit()]
        # todo: pretrain a lot of models
        word_generator = MarkovianWordLevelGenerator(numbers[0]).fit(word_level.TEXTS)
        generated_text = word_generator.generate_text()
        msg = bot.send_message(message.chat.id, generated_text)
        print(msg)
    except Exception as e:
        msg = bot.send_message(message.chat.id, "Oops, error " + str(e))
        print(msg)
        print(e)


if __name__ == "__main__":
    bot.polling()
