import random
from collections import deque
import re

class Dictogram(dict):
    def __init__(self, iterable=None):
        super(Dictogram, self).__init__()
        self.types = 0
        self.tokens = 0
        if iterable:
            self.update(iterable)
    def update(self, iterable):
        for item in iterable:
            if item in self:
                self[item] += 1
                self.tokens += 1
            else:
                self[item] = 1
                self.types += 1
                self.tokens += 1
    def count(self, item):
        if item in self:
            return self[item]
        return 0
    def return_random_word(self):
        random_key = random.sample(self, 1)
        return random_key[0]
    def return_weighted_random_word(self):
        random_int = random.randint(0, self.tokens-1)
        index = 0
        list_of_keys = list(self.keys())
        for i in range(0, self.types):
            index += self[list_of_keys[i]]
            if(index > random_int):
                return list_of_keys[i]


def make_markov_model(data):
    markov_model = dict()

    for i in range(0, len(data)-1):
        if data[i] in markov_model:
            markov_model[data[i]].update([data[i+1]])
        else:
            markov_model[data[i]] = Dictogram([data[i+1]])
    return markov_model

begin = []

def generate_random_start(model):
    return random.choice(begin)
    if 'END' in model:
        seed_word = 'END'
        while seed_word == 'END':
            seed_word = model['END'].return_weighted_random_word()
        return seed_word
    return random.choice(list(model.keys()))


def generate_random_sentence(length, markov_model):
    #print(markov_model)
    current_word = generate_random_start(markov_model)
    sentence = [current_word]
    for i in range(0, length):
        current_dictogram = markov_model[current_word]
        random_weighted_word = current_dictogram.return_weighted_random_word()
        current_word = random_weighted_word
        sentence.append(current_word)
    sentence[0] = sentence[0].capitalize()
    return ' '.join(sentence) + '.'

file = open('base.txt', 'r', encoding='utf-8')
text = file.read()
text = text.split()

alp = set()
mas = ['.', ',', '?', '!', '-', ':', '=', '+', '-', '*', '/', ':', ';']
for i in range(ord('a'), ord('z') + 1):
    alp.add(chr(i))
for i in range(ord('A'), ord('Z') + 1):
    alp.add(chr(i))
for i in mas:
    alp.add(i)
for i in range(ord('а'), ord('п') + 1):
    alp.add(chr(i))
for i in range(ord('р'), ord('я') + 1):
    alp.add(chr(i))
for i in range(ord('А'), ord('Я') + 1):
    alp.add(chr(i))
alp.add('ё')
alp.add('Ё')

for i in range(len(text)):
    res = ""
    for j in range(len(text[i])):
        if text[i][j] in alp:
            res += text[i][j]
        #if text[i][j] in ['.', '?', '!']:
         #   begin.append(text[i + 1])
    if len(res):
        text[i] = res

begin.append(text[0])
for i in range(len(text)):
    for j in range(len(text[i])):
        if text[i][j] in ['.', '?', '!']:
            begin.append(text[i + 1])

result = generate_random_sentence(8, make_markov_model(text))

print(result)