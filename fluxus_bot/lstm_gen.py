# coding:utf-8

import pickle
from fluxus_bot.log_config import *
import numpy as np

from keras.models import load_model

loaded_model = load_model("lstm_char_iter_2.model.h5")
char_indices = pickle.load(open("ch2i.bin", "rb"))
indices_char = pickle.load(open("i2ch.bin", "rb"))


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def lstm_generate(model=loaded_model, diversity=0.1):
    lg.info("Generating with diversity = " + str(diversity))

    generated = ''
    # sentence = text[start_index: start_index + maxlen]
    sentence = " " * 31 + "[s]  <n> "
    generated += sentence

    while len(generated) < 500 and (len(generated) < 250 or not "[e]" in generated):

        x = np.zeros((1, len(sentence), len(char_indices)))

        for t, char in enumerate(sentence):
            x[0, t, char_indices[char]] = 1.

        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char

    lg.info(generated)

    generated = generated.replace("[s]", "").replace("[e]", "").replace("<n>", "\n").strip()

    lg.info(generated)

    return generated


generate()
