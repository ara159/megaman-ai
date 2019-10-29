#!env/bin/python3

import tensorflow as tf
import keras
from sys import argv
from tensorflow.python.util import deprecation
from os import environ

# disable warning messages
deprecation._PRINT_DEPRECATION_WARNINGS = False
environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

print("[*] Criando nova rede recorrente")
steps = 15

modelo = keras.Sequential([
        keras.layers.LSTM(500, input_shape=(steps, 2016), return_sequences=True),
        keras.layers.Dropout(0.2),
        keras.layers.LSTM(250),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(100),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(20, activation=keras.activations.softmax),
    ])
modelo.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])

print("[*] Rede criada")
modelo.save("modelos/exemplo.h5")

print("[!] Rede \"exemplo\" salva!")
modelo.summary()
