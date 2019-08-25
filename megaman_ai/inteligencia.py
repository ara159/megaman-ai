from os import path

import tensorflow as tf
from tensorflow import keras

# Variáveis globais
_caminho = "modelos/" # caminho do arquivo modelo
modelo = None # O modelo que carregado

def carregar(nome, num_classes):
    """Carrega o modelo em caminho e atualiza o modelo carregado. Se o arquivo
     existe: Carrega o modele. Se não existe existe: Cria um novo modelo"""
    global modelo, _caminho
    
    _caminho += nome

    if path.isfile(nome):
        modelo = keras.models.load_model(nome)
    else:
        modelo = keras.Sequential([
                keras.layers.Flatten(input_shape=(240, 256)),
                keras.layers.Dense(128, activation=tf.nn.relu),
                keras.layers.Dense(64, activation=tf.nn.relu),
                keras.layers.Dense(num_classes * 2, activation=tf.nn.softmax),
            ])

        modelo.compile(
                optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'], verbose=0)

def salvar():
    """Salva o modelo carregado atualmente em aquivo"""
    global modelo, _caminho
    
    modelo.save(_caminho)
