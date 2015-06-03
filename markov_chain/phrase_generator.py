#!/usr/bin/python3.4
"""
Description:

Learning Markov chain part

Usage:
  phrase_generator <words> ... [--n <num>]
  phrase_generator -h | --help

Options:
  -h --help     Show this screen.
  --n=num       Number of words to complement
"""
import pickle
from random import randint
from os import path

from docopt import docopt
from schema import Schema, Use, Optional


def main():
    args = docopt(__doc__)
    schema = Schema({
        '--n': Use(int),
        Optional('--help'): object,
        '<words>': object,
    })
    args = schema.validate(args)
    num_of_words = args['--n']
    words = args['<words>']
    order = len(words)
    chain = load_chain_from_file(order)
    phrase = ' '.join(words)
    for i in range(num_of_words):
        word = get_next_word(chain, ' '.join(words[-order:]))
        if word:
            phrase = ' '.join([phrase, word])
            words.append(word)
        else:
            break
    print(phrase)


def load_chain_from_file(order):
    """
    Загружает цепь из файла, при наличии цепи соответствующего порядка. Иначе прерывает работу.
    """
    data_dir = path.join(path.dirname(path.abspath(__file__)), 'data')
    filename = data_dir + '/chain_' + str(order) + '.pkl'
    if not path.isfile(filename):
        print('Вероятно, цепь {0}-порядка еще не создана'.format(order))
        exit()
    with open(filename, 'rb') as f:
        return pickle.load(f)


def get_next_word(chain, phrase_part):
    """
    Возвращает следющее случайное слово из возможных за заданной фразой. Вероятность пропорциональна частоте.
    Длина фразы должна быть равна порядку цепи.
    """
    possible_words = chain.get(phrase_part, '')
    if not possible_words:
        return
    rand = randint(1, sum(possible_words.values()))
    for word, weigth in possible_words.items():
        rand -= weigth
        if rand <= 0:
            return word

if __name__ == '__main__':
    main()