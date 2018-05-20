import string
import random
import numpy as np
from random import shuffle, sample

def read_text_file(text_file_name, remove_chars):
    with open(text_file_name, 'r') as file:
        file_arr = []
        for line in file.read().splitlines():
            line = line.translate(None, remove_chars)
            words_arr = [line.strip() for line in line.split(' ') if line.strip()]
            file_arr.extend(words_arr)
        return np.array(file_arr)


def calculate_probability(p):
    return random.random() >= 1-p


class GeneticAlgorithm:

    def __init__(self, population_size, possible_chars, enc, dict, mutation_rate):
        self.population_size = population_size
        self.possible_chars = possible_chars
        self.enc = enc
        self.dict = dict
        self.mutation_rate = mutation_rate

        self.population = self.initialize_population()

    def initialize_population(self):
        population = []
        for x in range(self.population_size):
            permutation = {}
            values = ''.join(sample(self.possible_chars, len(self.possible_chars)))
            for i, char in enumerate(self.possible_chars):
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

    def find_key_by_letter_in_dict(self, letter):
        return [key for key, value in self.dict.iteritems() if value == letter][0]

    def mutate(self, permutation):
        for letter in permutation:
            if calculate_probability(self.mutation_rate):
                random_letter = random.choice(string.ascii_letters)

                key_of_random_letter = self.find_key_by_letter_in_dict(random_letter)
                permutation[key_of_random_letter] = permutation[letter]

                permutation[letter] = random_letter

    def train(self):
        print "Starting training"

        print self.fitness(self.population[0])


if __name__ == "__main__":

    enc1 = read_text_file("enc1.txt", ".,;")
    enc2 = read_text_file("enc2.txt", "")
    dict = np.loadtxt("dict.txt", dtype=np.str, encoding='iso 8859-1')

    population_size = 50
    enc1_chars = string.ascii_lowercase
    mutation_rate = 0.005

    GA1 = GeneticAlgorithm(population_size, enc1_chars, enc1, dict, mutation_rate)

    GA1.train()

    # enc2_chars = string.ascii_lowercase + " .,;"
    # GA2 = GeneticAlgorithm(population_size, enc2_chars, enc2, dict)

