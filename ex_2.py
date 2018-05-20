import string
import numpy as np
from random import shuffle, sample
import operator

def read_text_file(text_file_name, remove_chars):
    with open(text_file_name, 'r') as file:
        file_arr = []
        for line in file.read().splitlines():
            line = line.translate(None, remove_chars)
            words_arr = [line.strip() for line in line.split(' ') if line.strip()]
            file_arr.extend(words_arr)
        return np.array(file_arr)


class GeneticAlgorithm:

    def __init__(self, population_size, replication_rate, possible_chars, enc, dict):
        self.population_size = population_size
        self.replication_rate = replication_rate
        self.possible_chars = possible_chars
        self.enc = enc
        self.dict = dict

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

    def replication(self, sorted_permutations):
        print sorted_permutations
        top_permutaions = sorted_permutations[:int(self.replication_rate * population_size)]
        print [self.population[index] for index in top_permutaions]

    def calculate_population_fitness(self):
        fitness_dict = {}
        for i, permutation in enumerate(self.population):
            fitness_dict[i] = self.fitness(permutation)
        sorted_permutations = [k for k in sorted(fitness_dict, key=fitness_dict.get, reverse=True)]
        # print fitness_dict
        return sorted_permutations

    def train(self):
        print "Starting training"
        new_population = []

        sorted_permutations = self.calculate_population_fitness()

        new_population.extend[self.replication(sorted_permutations)]


if __name__ == "__main__":

    enc1 = read_text_file("enc1.txt", ".,;")
    print enc1
    enc2 = read_text_file("enc2.txt", "")
    dict = np.loadtxt("dict.txt", dtype=np.str, encoding='iso 8859-1')

    population_size = 50
    replication_rate = 0.05
    enc1_chars = string.ascii_lowercase
    GA1 = GeneticAlgorithm(population_size, replication_rate, enc1_chars, enc1, dict)

    GA1.train()

    # enc2_chars = string.ascii_lowercase + " .,;"
    # GA2 = GeneticAlgorithm(population_size, enc2_chars, enc2, dict)

