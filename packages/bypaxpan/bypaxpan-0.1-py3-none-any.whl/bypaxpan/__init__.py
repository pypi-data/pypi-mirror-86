#!/usr/bin/env python3
from spacy import load
from random import randint
from pysinonimos.sinonimos import Search

nlp = load('pt_core_news_sm')

def getAdv(text):
    doc = nlp(text)
    word = []
    for token in doc:
        if token.pos_ == "ADV":
            word.append(token.orth_)
    return word

def randonize(text):
    advs = getAdv(text)
    word = advs[randint(0, len(advs) - 1)]
    synonyms = Search(word).synonyms()
    return text.replace(word, synonyms[randint(0, len(synonyms) - 1)])

