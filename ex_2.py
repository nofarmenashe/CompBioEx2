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
        return [self.population[index] for index in top_permutaions]

    def create_permutation_array_by_fitness(self, fitness_dictionary):
        permutations_array = []
        for per, fitness in fitness_dictionary.items():
            permutations_array.extend(np.full(fitness, per))
        return permutations_array

    def chooseParents(self, fitness_array):
        first, second = np.random.randint(0, len(fitness_array), 2)
        return fitness_array[first], fitness_array[second]

    def create_child(self, pf1, pf2):
        probability_of_p1 = float(pf1["fitness"]) / (pf1["fitness"] + pf2["fitness"])
        print pf1["fitness"],  pf2["fitness"], " p = ", probability_of_p1
        new_permutation = {}
        chars_without_permutation = pf1["permutation"].keys()
        chars_left = pf1["permutation"].keys()
        # print pf1["permutation"]
        # print pf2["permutation"]
        # print zip(pf1["permutation"], pf2["permutation"])
        for c, per1, per2 in zip(pf1["permutation"].keys(), pf2["permutation"].values(), pf1["permutation"].values()):
            if np.random.random() < probability_of_p1:  # choose from first parent
                print c, per1, per2, "1"
                if per1 in chars_left:
                    new_permutation[c] = per1
                    chars_left.remove(per1)
                    chars_without_permutation.remove(c)
            else:  # choose from second parent
                print c, per1, per2, "2"
                if per2 in chars_left:
                    new_permutation[c] = per2
                    chars_left.remove(per2)
                    chars_without_permutation.remove(c)

        for i, c in enumerate(chars_without_permutation):
            print c, "?"
            new_permutation[c] = chars_left[i]

        print new_permutation
        return new_permutation

    def crossover(self, fitness_dictionary):
        fitness_array = self.create_permutation_array_by_fitness(fitness_dictionary)
        new_gen_crossover = []
        for i in range(int((1 - self.replication_rate) * population_size)):
            parent1_index, parent2_index = self.chooseParents(fitness_array)
            parent_fitness_1 = {"permutation": self.population[parent1_index], "fitness": fitness_dictionary[parent1_index]}
            parent_fitness_2 = {"permutation": self.population[parent2_index], "fitness": fitness_dictionary[parent2_index]}
            new_gen_crossover.append(self.create_child(parent_fitness_1, parent_fitness_2))
        return new_gen_crossover

    def calculate_population_fitness(self, fitness_dict):
        sorted_permutations = [k for k in sorted(fitness_dict, key=fitness_dict.get, reverse=True)]
        self.crossover(fitness_dict)
        # print fitness_dict
        return sorted_permutations

    def get_fitness_dictionary(self):
        fitness_dict = {}
        for i, permutation in enumerate(self.population):
            fitness_dict[i] = self.fitness(permutation)

    def train(self):
        print "Starting training"
        new_population = []

        fitness_dict = self.get_fitness_dictionary()
        sorted_permutations = self.calculate_population_fitness(fitness_dict)

        new_population.extend(self.replication(sorted_permutations))
        new_population.extend(self.crossover(fitness_dict))


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

