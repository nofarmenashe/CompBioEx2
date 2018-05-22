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

    def most_common_letter(self):
        letters_count = {}
        for char in self.possible_chars:
            letters_count[char] = 0

        for encrypted_word in self.enc:
            for c in encrypted_word:
                letters_count[c] += 1

        max_count = np.max(letters_count.values())
        for char in letters_count.keys():
            if letters_count[char] == max_count:
                return char


    def initialize_population(self):
        population = []
        common_letter = self.most_common_letter()
        for x in range(self.population_size):
            permutation = {}
            values = ''.join(sample(self.possible_chars, len(self.possible_chars)))
            for i, char in enumerate(self.possible_chars):
                permutation[char] = values[i]

            common_letter_key = self.find_key_by_letter_in_dict(permutation, common_letter)
            permutation[common_letter_key] = permutation['e']

            permutation['e'] = common_letter
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
        # print permutation
        for letter in permutation.keys():
            if calculate_probability(self.mutation_rate):
                random_letter = random.choice(string.ascii_lowercase)

                key_of_random_letter = self.find_key_by_letter_in_dict(permutation, random_letter)
                permutation[key_of_random_letter] = permutation[letter]

                permutation[letter] = random_letter

        # print permutation
        return permutation

    def replication(self, sorted_permutations):
        # print sorted_permutations
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
        new_permutation = {}
        chars_without_permutation = pf1["permutation"].keys()
        chars_left = pf1["permutation"].keys()
        for c, per1, per2 in zip(pf1["permutation"].keys(), pf1["permutation"].values(), pf2["permutation"].values()):
            if np.random.random() < probability_of_p1:  # choose from first parent
                if per1 in chars_left:
                    new_permutation[c] = per1
                    chars_left.remove(per1)
                    chars_without_permutation.remove(c)
            else:  # choose from second parent
                if per2 in chars_left:
                    new_permutation[c] = per2
                    chars_left.remove(per2)
                    chars_without_permutation.remove(c)

        shuffle(chars_left)
        for i, c in enumerate(chars_without_permutation):
            new_permutation[c] = chars_left[i]

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
        # self.crossover(fitness_dict)
        # print fitness_dict
        return sorted_permutations

    def get_fitness_dictionary(self):
        fitness_dict = {}
        for i, permutation in enumerate(self.population):
            fitness_dict[i] = self.fitness(permutation)
        return fitness_dict

    def train(self):
        print "Starting training"
        # new_fitness = [self.fitness(permutation) for permutation in self.population]
        # new_fitness = [0]

        expected_result = len(self.enc)
        best_fitness = 0

        while best_fitness < expected_result:
            new_population = []

            fitness_dict = self.get_fitness_dictionary()
            sorted_permutations = self.calculate_population_fitness(fitness_dict)
            best_fitness = fitness_dict[sorted_permutations[0]]
            best_permutation = self.population[sorted_permutations[0]]

            new_population.extend(self.replication(sorted_permutations))
            new_population.extend(self.crossover(fitness_dict))

            new_population.remove(best_permutation)
            new_population = [self.mutate(permutation) for permutation in new_population]
            new_population.append(best_permutation)

            # new_fitness = [self.fitness(per) for per in new_population]
            new_fitness = fitness_dict.values()

            print "best", np.max(new_fitness)
            print "avg", np.average(new_fitness)

            self.population = new_population


if __name__ == "__main__":

    enc1 = read_text_file("enc1.txt", ".,;")
    enc2 = read_text_file("enc2.txt", "")
    dict = np.loadtxt("dict.txt", dtype=np.str, encoding='iso 8859-1')

    population_size = 100
    replication_rate = 0.05
    enc1_chars = string.ascii_lowercase
    mutation_rate = 0.02

    GA1 = GeneticAlgorithm(population_size, replication_rate, mutation_rate, enc1_chars, enc1, dict)

    GA1.train()

    # enc2_chars = string.ascii_lowercase + " .,;"
    # GA2 = GeneticAlgorithm(population_size, enc2_chars, enc2, dict)

