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
        "Это FLUXUS-бот.\n Доступные команды:\n   "
        "/random -- случайный перформанс\n   "
        "/markov <char/word> <depth> -- сгенерированный марковской цепью перформанс\n"
        "\nПример: /markov char 8"
        "\n        /markov word 2"
        "\n        /random"
        "\n\nЧем больше \"глубина\" цепи, тем осмысленнее получится текст, "
        "но тем больше и шансы, что он полностью скопирован цепью из книжки.\n\n"
        "Бот разработан к перформансу в Санкт-Петербургском Музее звука:\n"
        "24 июня 2017, 20:00. FLUXUS СПб: программа звуковых перформансов ")
    print("Response:", msg)


@bot.message_handler(commands=['random'])
def send_random(message):
    random_score = scores[random.randint(0, len(scores))]
    msg = bot.send_message(message.chat.id, random_score)
    print(msg)


@bot.message_handler(regexp="/markov char \d+")
def send_markov_char(message):
    numbers = [int(s) for s in message.text.split() if s.isdigit()]
    # todo: pretrain a lot of models
    char_generator = MarkovianCharLevelGenerator(numbers[0]).fit(char_level.TEXTS)
    generated_text = char_generator.generate_text()
    msg = bot.send_message(message.chat.id, generated_text)
    print(msg)


@bot.message_handler(regexp="/markov word \d+")
def send_markov_char(message):
    numbers = [int(s) for s in message.text.split() if s.isdigit()]
    # todo: pretrain a lot of models
    word_generator = MarkovianWordLevelGenerator(numbers[0]).fit(word_level.TEXTS)
    generated_text = word_generator.generate_text()
    msg = bot.send_message(message.chat.id, generated_text)
    print(msg)

if __name__ == "__main__":
    bot.polling()
