import string
import numpy as np
from random import shuffle, sample

import numpy as np
from numpy import random

def read_text_file(text_file_name):
    with open(text_file_name, 'r') as file:
        file_arr = []
        for line in file.read().splitlines():
            words_arr = [line.strip() for line in line.split(' ') if line.strip()]
            file_arr.extend(words_arr)
        return np.array(file_arr)


def initialize_parameters():
    permutation = {}
    values = random.shuffle(string.ascii_lowercase)
    for char in string.ascii_lowercase:
        permutation[char] = char
    return permutation


class GeneticAlgorithm:

    def __init__(self, population_size, enc, dict):
        self.population_size = population_size
        self.enc = enc
        self.dict = dict

        self.population = self.initialize_population()

    def initialize_population(self):
        population = []
        for x in range(self.population_size):
            permutation = {}
            values = ''.join(sample(string.ascii_lowercase,len(string.ascii_lowercase)))
            for i, char in enumerate(string.ascii_lowercase):
                permutation[char] = values[i]
            population.append(permutation)
        return population

    def permutated_word(self, permutation, encrypted_word):
        real_word = ""
        for letter in encrypted_word:
            real_word += permutation[letter]
        return real_word

    def is_fit(self, permutation, encrypted_word):
        permutated_word = self.permutated_word(permutation, encrypted_word)
        for word in dict:
            if word == permutated_word:
                return True

        return False

    def fitness(self, permutation):
        success_count = 0
        for encrypted_word in self.enc:
            if self.is_fit(permutation, encrypted_word):
                success_count += 1

        return success_count

    def train(self):
        print "Starting training"

        print self.population[0]
        print self.fitness(self.population[0])


if __name__ == "__main__":

    enc1 = read_text_file("enc1.txt")
    enc2 = read_text_file("enc2.txt")
    dict = np.loadtxt("dict.txt", dtype=np.str, encoding='iso 8859-1')

    population_size = 3

    GA = GeneticAlgorithm(population_size, enc1, dict)

    GA.train()
