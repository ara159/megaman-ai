#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 18:44:29 2019

@author: rafael
"""

import numpy as np
import yaml

from megaman_ai import visao
from matplotlib import pyplot as plt

# pega o nome
nome = "ffDropOut512-128-20p02-copia"

# Carrega o log
log = yaml.load(open("logs/{}.log".format(nome), "r").read())

def plt_rotulos(rotulos):    
    clss = visao.MegaMan(yaml.load(open("megaman.yaml", "r").read())).classes
    roto, count = np.unique(rotulos, return_counts=True)
    plt.title("Distribuição dos rótulos usados")
    plt.ylabel("quantidade")
    plt.xlabel("rótulo")
    plt.hist(np.asarray(rotulos), 20, label=np.array(clss))
    plt.show()
    
acc = np.array([])
loss = np.array([])
rotulos = np.array([])

for fit in list(log.keys()):
    rotulos = np.concatenate((rotulos, log[fit]['rotulos']))
    acc = np.concatenate((acc, log[fit]['acc']))
    loss = np.concatenate((loss, log[fit]['loss']))
    
plt.title("rotulos")
plt.hist(rotulos, 20)
plt.show()

plt.title("acc")
plt.plot(acc)
plt.show()

plt.title("loss")
plt.plot(loss)
plt.show()
