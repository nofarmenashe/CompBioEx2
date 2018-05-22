import string
import random
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


def calculate_probability(p):
    return random.random() >= 1-p


class GeneticAlgorithm:

    def __init__(self, population_size, replication_rate, mutation_rate, possible_chars, enc, dict):
        self.population_size = population_size
        self.replication_rate = replication_rate
        self.mutation_rate = mutation_rate

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

    def find_key_by_letter_in_dict(self, permutation, search_letter):
        for key in permutation.keys():
            if permutation[key] == search_letter:
                return key

    def mutate(self, permutation):
        print permutation
        for letter in permutation.keys():
            if calculate_probability(self.mutation_rate):
                random_letter = random.choice(string.ascii_lowercase)

                key_of_random_letter = self.find_key_by_letter_in_dict(permutation, random_letter)
                permutation[key_of_random_letter] = permutation[letter]

                permutation[letter] = random_letter

        print permutation
        return permutation

    def replication(self, sorted_permutations):
        print sorted_permutations
        top_permutations = sorted_permutations[:int(self.replication_rate * population_size)]
        # print [self.population[index] for index in top_permutations]
        return top_permutations

    def crossover(self):
        self.createArray

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

        new_population.extend(self.replication(sorted_permutations))

        self.mutate(self.population[0])


if __name__ == "__main__":

    enc1 = read_text_file("enc1.txt", ".,;")
    enc2 = read_text_file("enc2.txt", "")
    dict = np.loadtxt("dict.txt", dtype=np.str, encoding='iso 8859-1')

    population_size = 50
    replication_rate = 0.05
    enc1_chars = string.ascii_lowercase
    mutation_rate = 0.05

    GA1 = GeneticAlgorithm(population_size, replication_rate, mutation_rate, enc1_chars, enc1, dict)

    GA1.train()


    # enc2_chars = string.ascii_lowercase + " .,;"
    # GA2 = GeneticAlgorithm(population_size, enc2_chars, enc2, dict)

