import csv
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

# Set up character-index dictionaries
char_to_index = dict()
index_to_char = dict()
char_CSV_file = "supported_characters.csv"
with open(char_CSV_file, newline="") as char_CSV:
    char_csv_reader = csv.reader(char_CSV)
    i = 0
    char_to_index["$"] = i
    index_to_char[i] = "$"
    for row in char_csv_reader:
        i += 1
        char_to_index[row] = i
        index_to_char[i] = row

# Set up samples
sample_CSV = ""
sample_names = []
with open(sample_CSV, newline="") as CSV_file:
    sample_reader = csv.reader(CSV_file)
    for row in sample_reader:
        sample_names.append(row[0] + "$")

# Length of longest name to be generated
max_char = len(max(sample_names, key=len))
# Number of possible characters to be included in generated names
potential_char_num = len(char_to_index)
# Number of elements in list of sample names
training_names_num = len(sample_names)

# Create training dataset from sample
X = np.zeroes((training_names_num, max_char, potential_char_num))
Y = np.zeroes((training_names_num, max_char, potential_char_num))
for i in range(training_names_num):
    name = sample_names[i]
    for j in range(len(name)):
        X[i, j, char_to_index[name[j]]] = 1
        if j < len(name) - 1:
            Y[i, j, char_to_index[name[j+1]]] = 1

model = keras.Sequential()
model.add(layers.LSTM(128, input_shape=(max_char, potential_char_num), ))
model.add(layers.Dense(potential_char_num))
