"""
Arquivo auxiliar para criação da rede neural.

O código abaixo é um exemplo de como se criar a RN.

A camada de entrada deve ter exatamente o tamanho indicado.
A saida deve ter exatamente o tamanho indicado.

O restante pode ser configurado como queira.

A função de compile pode ter parâmetros personalizados também.

O exemplo é funcional, apenas descomente e rode.
"""

import tensorflow as tf
from tensorflow import keras

nome = "ff01.h5"

modelo = keras.Sequential([
        keras.layers.Flatten(input_shape=(240, 256)),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dropout
        keras.layers.Dense(64, activation=tf.nn.relu),
        keras.layers.Dense(20, activation=tf.nn.softmax),
    ])

modelo.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])

modelo.save("modelos/"+nome)