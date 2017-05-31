# -*- coding: utf-8 -*-

import configparser
import telebot
import random

config_parser = configparser.ConfigParser()
config_parser.read("configs/bot.ini")
token = config_parser.get("Credentials", "ApiToken")
bot = telebot.TeleBot(token)

scores = [line.replace("<n>", "\n").replace("[S]", "").replace("[E]", "") for line in open("../fluxus_parsing2/parsed_texts.txt")]

print("Bot started.")


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.send_message(
        message.chat.id,
        "Это FLUXUS-бот.\n Доступные команды:\n   /random\n   /generate_markov_2")
    print("Response:", msg)


@bot.message_handler(commands=['random'])
def send_random(message):
    random_score = scores[random.randint(0, len(scores))]
    msg = bot.send_message(message.chat.id, random_score)
    print(msg)


@bot.message_handler(commands=['generate_markov_2'])
def send_markov2(message):
    msg = bot.send_message(message.chat.id, "Oops! Not implemented yet!")
    print(msg)

if __name__ == "__main__":
    bot.polling()
