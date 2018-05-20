import json
import numpy as np

def read_text_file(text_file_name):
    with open(text_file_name, 'r') as file:
        file_arr = []
        for line in file.read().splitlines():
            words_arr = [line.strip() for line in line.split(' ') if line.strip()]
            file_arr.extend(words_arr)
        return np.array(file_arr)

enc1 = read_text_file("enc1.txt")
enc2 = read_text_file("enc2.txt")
dict = np.loadtxt("dict.txt", dtype=np.str)
