from random import randint
import json

from .dictionary import DICTIONARY
from .utils import max_siblings_vowels, max_siblings_consonants

class Nouns:
    def filter(self):
        self.nouns = [
            word
            for word in self.dictionary
            if (
                len(word) > 3
                and max_siblings_vowels(word, 2)
                and max_siblings_consonants(word, 2)
            )
        ]
        self.length = len(self.nouns)

    def random_noun(self):
        n = randint(0, self.length)
        return self.nouns[n]

    def generate(self):
        noun1 = self.random_noun()
        noun2 = self.random_noun()

        random_name = noun1[: randint(0, len(noun1))] + noun2[randint(0, len(noun2)) :]
        return random_name

    def __init__(self):
        self.dictionary = DICTIONARY
        self.filter()
