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
        "Я — <b>FLUXUS-бот</b>, добрый день!\n\n<b>Доступные команды:</b>\n"
        " /random \n  случайный оригинальный перформанс\n"
        " /markov {char/word} {depth} \n  сгенерированный марковской цепью перформанс\n"
        " /about  \n  о боте\n"
        "\n<b>Примеры:</b>"
        "\n    /markov char 8"
        "\n    /markov word 2"
        "\n    /random"
        "\n\nЧем больше \"глубина\" цепи, тем осмысленнее получится текст, "
        "но тем больше шансы, что он полностью скопирован цепью из книжки.\n\n"
        "Бот разработан в рамках подготовки к перформансу\n"
        "в <a href=\"https://vk.com/soundmuseumspb\">Санкт-Петербургском Музее звука:</a>\n\n"
        "<b>24 июня 2017, 20:00</b>\nFLUXUS СПб: программа звуковых перформансов\n\n"
        "<b>Приходите!</b>", parse_mode="HTML")
    print("Response:", msg)


@bot.message_handler(commands=['about'])
def send_about(message):
    msg = bot.send_message(
        message.chat.id,
        "Бот разработан в рамках подготовки к перформансу\n"
        "в <a href=\"https://vk.com/soundmuseumspb\">Санкт-Петербургском Музее звука:</a>\n"
        "<b>24 июня 2017, 20:00. FLUXUS СПб: программа звуковых перформансов</b>\n\n"
        "<b>Приходите!</b>\n\n"
        "Спонтанность можно перенести на новый уровень, сгенерировав инструкцию к перформансу перед самим перформансом."
        "В качестве механизма генерации были выбраны простые марковские цепи для слов и символов. "
        "Вероятности переходов -- относительные частоты соответствующих нграм оригинальных инструкций.\n\n"
        "<a href=\"http://soundmuseumspb.ru/\">Сайт музея</a>\n"
        "<a href=\"https://vk.com/soundmuseumschool\">Школа импровизационной музыки</a>\n"
        "<a href=\"http://alexeyev.github.io/\">Об авторе</a>", parse_mode="HTML")
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
