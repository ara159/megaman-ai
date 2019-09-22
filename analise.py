#!env/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 18:44:29 2019

@author: rafael
"""

import numpy as np
import yaml
from sys import argv
from megaman_ai import visao
from matplotlib import pyplot as plt

# pega o nome
if len(argv) > 1:
    nome = argv[1]
else:
    nome = "ffRafael"

# Carrega o log
log = yaml.load(open("logs/{}.log".format(nome), "r").read())

def graf_rot():
    # Carrega os dados
    dd = np.array([])
    for data in log.keys():
        dd = np.concatenate((dd,log[data]['rotulos']))
        
    # Rótulos
    mm = visao.MegaMan(yaml.load(open("megaman.yaml", "r").read()))
    rr,qq = np.unique(dd, return_counts=True)
    cc = ["("+str(int(i))+") "+mm.classes[int(i)] for i in rr]
    
    plt.figure(figsize=(12,12))
    wedges, texts, autotexts = plt.pie(qq, autopct='%1.1f%%')
    plt.legend(wedges, cc, title="Rótulos")
    plt.show()

def graf_acc():
    aa = np.array([])
    mm = [],[]
    su = 0
    
    for i,data in enumerate(log.keys()):
        su += len(log[data]['acc'])
        aa = np.concatenate((aa, log[data]['acc']))
        mm[0].append(su)
        mm[1].append(np.mean(log[data]['acc']))
        
    plt.plot(aa)
    plt.plot(mm[0], mm[1])
    plt.xlabel("epoch")
    plt.ylabel("acc")
    plt.show()

def graf_loss():
    ll = np.array([])
    mm = [],[]
    su = 0
    
    for i,data in enumerate(log.keys()):
        su += len(log[data]['loss'])
        ll = np.concatenate((ll, log[data]['loss']))
        mm[0].append(su)
        mm[1].append(np.mean(log[data]['loss']))
        
    plt.plot(ll)
    plt.plot(mm[0], mm[1])
    plt.xlabel("epoch")
    plt.ylabel("loss")
    plt.show()

if len(argv) >= 3:
    if "acc" in argv:
        graf_acc()
    if "rot" in argv:
        graf_rot()
    if "loss" in argv:
        graf_loss()
        
else:
    graf_rot()
    graf_acc()
    graf_loss()
