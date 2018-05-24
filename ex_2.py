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


def read_text_file_by_lines(text_file_name):
    with open(text_file_name, 'r') as file:
        file_arr = []
        for line in file.read().splitlines():
            if line.strip():
                file_arr.append(line)
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
        # common_letter = self.most_common_letter()
        for x in range(self.population_size):
            permutation = {}
            values = ''.join(sample(self.possible_chars, len(self.possible_chars)))
            for i, char in enumerate(self.possible_chars):
                permutation[char] = values[i]

            # common_letter_key = self.find_key_by_letter_in_dict(permutation, common_letter)
            # permutation['e'] = permutation[common_letter_key]
            #
            # permutation[common_letter] = 'e'
            population.append(permutation)

        return population

    def permutated_word(self, permutation, encrypted_word):
        real_word = ""
        for letter in encrypted_word:
            if letter in self.possible_chars:
                real_word += permutation[letter]
            else:
                real_word += letter
        return real_word

    def is_fit(self, permutation, encrypted_word):
        permutated_word = self.permutated_word(permutation, encrypted_word)
        if permutated_word in dict:
                return True
        return False

    def fitness(self, permutation, *positional_parameters, **keyword_parameters):

        words = self.enc
        if 'words' in keyword_parameters:
            words = keyword_parameters['words']

        success_count = 0
        for encrypted_word in words:
            if self.is_fit(permutation, encrypted_word):
                success_count += 1

        return success_count

    def find_key_by_letter_in_dict(self, permutation, search_letter):
        for key in permutation.keys():
            if permutation[key] == search_letter:
                return key

    def mutate(self, population):
        # print permutation
        for permutation in population:
            if calculate_probability(self.mutation_rate):
                random_letter1, random_letter2 = np.random.choice(permutation.keys(), size=2)

                permutation_letter1 = permutation[random_letter1]
                permutation[random_letter1] = permutation[random_letter2]
                permutation[random_letter2] = permutation_letter1

        # print permutation
        return population

    def replication(self, sorted_permutations):
        # print sorted_permutations
        top_permutaions = sorted_permutations[:int(self.replication_rate * population_size)]
        return [self.population[index] for index in top_permutaions]

    # def create_permutation_array_by_fitness(self, fitness_dictionary):
    #     permutations_array = []
    #     sum_fitnesses = np.sum(fitness_dictionary.values())
    #     for per, fitness in fitness_dictionary.items():
    #         print fitness, sum_fitnesses
    #         permutations_array.extend(np.full(int(float(fitness) / sum_fitnesses), per))
    #     print permutations_array
    #     return permutations_array

    def chooseParents(self, fitness_dict):
        sum_of_fitnesses = np.sum(fitness_dict.values())
        fitness_probability = [float(f) / sum_of_fitnesses for f in fitness_dict.values()]
        first, second = np.random.choice(fitness_dict.keys(), size=2, p=fitness_probability)
        return first, second

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
        new_gen_crossover = []
        for i in range(int((1 - self.replication_rate) * population_size)):
            parent1_index, parent2_index = self.chooseParents(fitness_dictionary)
            parent_fitness_1 = {"permutation": self.population[parent1_index], "fitness": fitness_dictionary[parent1_index]}
            parent_fitness_2 = {"permutation": self.population[parent2_index], "fitness": fitness_dictionary[parent2_index]}
            new_gen_crossover.append(self.create_child(parent_fitness_1, parent_fitness_2))
        return new_gen_crossover

    def calculate_population_fitness(self, fitness_dict):
        sorted_permutations = [k for k in sorted(fitness_dict, key=fitness_dict.get, reverse=True)]
        return sorted_permutations

    def get_fitness_dictionary(self):
        fitness_dict = {}
        for i, permutation in enumerate(self.population):
            fitness_dict[i] = self.fitness(permutation)
        return fitness_dict

    def get_max_fitness(self):
        return len(self.enc)

    def is_best(self, best_permutation):
        return self.fitness(best_permutation) == self.get_max_fitness()

    def print_text(self, permutation):
        print self.permutated_word(permutation, self.enc)

    def train(self):
        print "Starting training"

        expected_result = self.get_max_fitness()
        bests = []
        avgs = []
        best_fitness = 0
        iteration_number = 1
        best_permutation = self.population[0]

        # while best_fitness < expected_result:
        while not self.is_best(best_permutation):
            new_population = []

            fitness_dict = self.get_fitness_dictionary()
            sorted_permutations = self.calculate_population_fitness(fitness_dict)
            best_fitness = fitness_dict[sorted_permutations[0]]
            best_permutation = self.population[sorted_permutations[0]]

            new_population.extend(self.replication(sorted_permutations))

            new_population.extend(self.crossover(fitness_dict))

            new_population.remove(best_permutation)
            new_population = self.mutate(new_population)
            new_population.append(best_permutation)

            # new_fitness = [self.fitness(per) for per in new_population]
            new_fitness = fitness_dict.values()

            print "*** Iteration Number: ", iteration_number
            print "best", np.max(new_fitness)
            print "avg", np.average(new_fitness)

            bests.append(np.max(new_fitness))
            avgs.append(np.average(new_fitness))

            self.population = new_population
            iteration_number += 1

            if iteration_number % 20 == 0:
                self.print_text(best_permutation)

        return best_permutation


def write_result_to_files(GA, enc_text, permutation, perm_filename, plain_filename):
    permutated_text = GA.permutated_word(permutation, enc_text)
    plain_file = open(plain_filename, "w")
    plain_file.write(permutated_text)
    plain_file.close()
    print permutation
    perm_file = open(perm_filename, "w")
    for per in np.sort(permutation.keys()):
        perm_file.write(per + " " + permutation[per] + "\n")
    perm_file.close()


class GeneticAlgorithm2(GeneticAlgorithm):

    def __init__(self, population_size, replication_rate, mutation_rate, possible_chars, enc, dict):
        GeneticAlgorithm.__init__(self, population_size, replication_rate, mutation_rate, possible_chars, enc, dict)

    def fitness(self, permutation):
        fitness = 0
        for sentence in self.enc:
            # we do permutated_word TWICE !!!

            permutated_sentence = self.permutated_word(permutation, sentence)
            # specials = '.,;' #etc
            # trans = string.maketrans(specials, ' '*len(specials))
            # permutated_sentence = permutated_sentence.translate(trans)
            permutated_sentence = permutated_sentence.translate(None, ".,;")
            # print permutated_sentence
            words = permutated_sentence.split(' ')

            for word in words:
                if word in self.dict:
                    fitness += np.power(len(word), 2)

            # fitness += GeneticAlgorithm.fitness(self, permutation, words=words)

        return fitness

    def is_best(self, best_permutation):
        words = []
        for sentence in self.enc:
            permutated_sentence = self.permutated_word(best_permutation, sentence)
            # specials = '.,;' #etc
            # trans = string.maketrans(specials, ' '*len(specials))
            # permutated_sentence = permutated_sentence.translate(trans)
            permutated_sentence = permutated_sentence.translate(None, ".,;")
            words = permutated_sentence.split(' ')

            for word in words:
                if len(word) > 0 and word not in dict:
                    print word
                    return False

        return True

    def print_text(self, permutation):
        for sentence in self.enc:
            print self.permutated_word(permutation, sentence)

    # def mutate(self, population):
    #     for permutation in population:
    #         for letter in self.possible_chars:
    #             if calculate_probability(self.mutation_rate):
    #                 random_letter = random.choice(self.possible_chars)
    #
    #                 key_of_random_letter = self.find_key_by_letter_in_dict(permutation, random_letter)
    #                 permutation[key_of_random_letter] = permutation[letter]
    #
    #                 permutation[letter] = random_letter
    #
    #     return population


if __name__ == "__main__":

    enc1 = read_text_file("enc1.txt", ".,;")
    enc2 = read_text_file_by_lines("enc2.txt")

    dict = set(np.loadtxt("dict.txt", dtype=np.str, encoding='iso 8859-1'))

    population_size = 500
    replication_rate = 0.1
    enc1_chars = string.ascii_lowercase
    mutation_rate = 0.25

    # GA1 = GeneticAlgorithm(population_size, replication_rate, mutation_rate, enc1_chars, enc1, dict)
    # chosen_premutation = GA1.train()
    # # GA1.train()
    #
    #
    # with open("enc1.txt", 'r') as file:
    #     enc1_text = file.read()
    #
    # write_result_to_files(GA1, enc1_text, chosen_premutation, "perm1.txt", "plain1.txt")

    population_size_2 = 1000
    replication_rate_2 = 0.6
    replication_rate_2 = 0.2
    mutation_rate_2 = 0.2

    enc2_chars = string.ascii_lowercase + " .,;"

    print population_size_2, replication_rate_2, mutation_rate_2
    GA2 = GeneticAlgorithm2(population_size_2, replication_rate_2, mutation_rate_2, enc2_chars, enc2, dict)
    chosen_premutation = GA2.train()
    # GA2.train()

    with open("enc2.txt", 'r') as file:
        enc2_text = file.read()

    write_result_to_files(GA2, enc2_text, chosen_premutation, "perm2.txt", "plain2.txt")

    # permutated_text = GA2.permutated_word(chosen_premutation, enc2_text)
    # print permutated_text
