#!/usr/bin/python3.4
"""
Description:

Learning Markov chain part

Usage:
  learning_chain <urls> ... [--n <order>]
  learning_chain -h | --help

Options:
  -h --help     Show this screen.
  --n=order
"""
import subprocess
import pickle
from os import path

from docopt import docopt
from schema import Schema, Optional


chain = {}


def main():
    args = docopt(__doc__)
    schema = Schema({
        Optional('--n'): object,
        Optional('--help'): object,
        '<urls>': object,
    })
    args = schema.validate(args)
    order = int(args['--n']) or 1  # порядок цепи, если не указон, то 1

    for url in args['<urls>']:
        s = 'curl {0}'.format(url)
        process = subprocess.Popen(s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (text, err) = process.communicate()
        for sentence in text.decode('utf-8').split('.'):
            sentence = normalize_string(sentence)
            append_chain_with_order(sentence, order)
    save_chain_to_file(order)


def normalize_string(input_string):
    """
    Удаляет сдвоенные пробелы и все символы кроме буквенных, цифр и пробела
    """
    input_string = ' '.join(input_string.split())
    return ''.join([l.lower() for l in input_string if l.isalpha() or l.isdigit() or l == ' '])


def append_chain(sentence):
    """
    Заполеняет цепь из переданной строки
    """
    s_list = sentence.split()
    for word in s_list:
        chain.setdefault(word, {})
    for i in range(len(s_list)):
        if i == len(s_list) - 1:
            continue
        chain[s_list[i]].setdefault(s_list[i+1], 0)
        chain[s_list[i]][s_list[i+1]] += 1


def append_chain_with_order(sentence, order):
    """
    Заполняет цепь n-го (order) порядка из переданной строки, если длина достаточна
    """
    s_list = sentence.split()
    for i in range(len(s_list)):
        if i + order >= len(s_list):
            return
        phrase = ' '.join(s_list[i:i+order])
        chain.setdefault(phrase, {})
        chain[phrase].setdefault(s_list[i+order], 0)
        chain[phrase][s_list[i+order]] += 1


def save_chain_to_file(order):
    """
    Сохряняет цепь в pickle-файл. Порядок цепи указывается в степени
    """
    data_dir = path.join(path.dirname(path.abspath(__file__)), 'data')
    with open(data_dir + '/chain_' + str(order) + '.pkl', 'wb') as f:
        pickle.dump(chain, f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    main()
