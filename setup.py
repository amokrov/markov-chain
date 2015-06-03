from os import path
from setuptools import setup, find_packages
from markov_chain import __version__ as VERSION


REQUIREMENTS = path.join(path.dirname(path.abspath(__file__)),
                         'requirements.txt')

setup(
    name='MarkovChainTextGenerator',
    version=VERSION,
    url='https://github.com/amokrov/markov-chain',
    author='Alexandr Mokrov',
    author_email='alexander.mokrov@gmail.com',
    description='Command line client for Markov chain text generator',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'learning_chain = markov_chain.learning_chain:main',
            'phrase_generator = markov_chain.phrase_generator:main'
        ]

    },
    install_requires=map(str.strip, open(REQUIREMENTS).readlines()),
)
