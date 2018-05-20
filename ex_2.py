import numpy as np

def flatten_enc(enc):
    enc = [line.split(" ") for line in enc]
    enc = [item for sublist in enc for item in sublist]
    return enc

enc1 = np.loadtxt("enc1.txt", delimiter='\n',  dtype=np.str)
enc1 = flatten_enc(enc1)

enc2 = np.loadtxt("enc2.txt", delimiter='\n',  dtype=np.str)
enc2 = flatten_enc(enc2)

dict = np.loadtxt("dict.txt", delimiter='\n',  dtype=np.str)


print enc1
# print enc2
# print dict
