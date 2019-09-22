#!env/bin/python3

import tensorflow as tf
import keras
from sys import argv
from tensorflow.python.util import deprecation
from os import environ

# disable warning messages
deprecation._PRINT_DEPRECATION_WARNINGS = False
environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

print("[*] Criando nova rede")

modelo = keras.Sequential([
        keras.layers.LSTM(1000, input_shape=(5, 2016), return_sequences=True),
        keras.layers.Dropout(0.1),
        keras.layers.LSTM(500),
        keras.layers.Dropout(0.1),
        keras.layers.Dense(100),
        keras.layers.Dropout(0.1),
        keras.layers.Dense(20, activation=keras.activations.softmax),
    ])
modelo.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])

print("[*] Rede criada")
print("[?] Nome da nova rede:", end=" ")
modelo.save("modelos/"+input()+".h5")

print("[!] Rede salva!")
modelo.summary()
