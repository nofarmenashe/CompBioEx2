import string
import numpy as np
from random import shuffle, sample


def read_text_file(text_file_name):
    with open(text_file_name, 'r') as file:
        file_arr = []
        for line in file.read().splitlines():
            words_arr = [line.strip() for line in line.split(' ') if line.strip()]
            file_arr.extend(words_arr)
        return np.array(file_arr)


class GeneticAlgorithm:
    def initialize_population(self):
        population_size = 3
        population = []
        for x in range(population_size):
            permutation = {}
            values = ''.join(sample(string.ascii_lowercase,len(string.ascii_lowercase)))
            for i, char in enumerate(string.ascii_lowercase):
                permutation[char] = values[i]
            population.append(permutation)
        return population

    def __init__(self):
        self.permutation = self.initialize_population()



if __name__ == "__main__":

    enc1 = read_text_file("enc1.txt")
    enc2 = read_text_file("enc2.txt")
    dict = np.loadtxt("dict.txt", dtype=np.str, encoding='iso 8859-1')

    population_size = 50

    GA1 = GeneticAlgorithm(population_size, enc1, dict)
