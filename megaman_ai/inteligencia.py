from os import path

import tensorflow as tf
from tensorflow import keras

# Variáveis globais
_caminho = "modelos/" # caminho do arquivo modelo
modelo = None # O modelo que carregado

def carregar(nome):
    """Carrega o modelo em caminho e atualiza o modelo carregado. Se o arquivo
     existe: Carrega o modele. Se não existe existe: Cria um novo modelo"""
    global modelo, _caminho
    _caminho += nome+".h5"
    modelo = keras.models.load_model(_caminho)

def salvar():
    """Salva o modelo carregado atualmente em aquivo"""
    global modelo, _caminho
    
    modelo.save(_caminho)
