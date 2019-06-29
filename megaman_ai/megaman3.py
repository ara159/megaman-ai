from time import sleep
from server.python_server import *

controle_nes = {
    "start": 
        {"A" : False, "B": False, "down": False, "right":False, "select":False, "start":True, "up":False, "left": False},
    "select": 
        {"A" : False, "B": False, "down": False, "right":False, "select":True, "start":False, "up":False, "left": False},
    "esquerda": 
        {"A" : False, "B": False, "down": False, "right":False, "select":False, "start":False, "up":False, "left": True},
    "direita": 
        {"A" : False, "B": False, "down": False, "right":True, "select":False, "start":False, "up":False, "left": False},
    "cima": 
        {"A" : False, "B": False, "down": False, "right":False, "select":False, "start":False, "up":True, "left": False},
    "baixo": 
        {"A" : False, "B": False, "down": True, "right":False, "select":False, "start":False, "up":False, "left": False},
    "A": 
        {"A" : True, "B": False, "down": False, "right":False, "select":False, "start":False, "up":False, "left": False},
    "B": 
        {"A" : False, "B": True, "down": False, "right":False, "select":False, "start":False, "up":False, "left": False},
}

class MegaMan3:
    def __init__(self, emulador):
        self.emulador = emulador

    def iniciar(self):
        self._esperar(6)
        joypad.write(1, controle_nes["start"])
        self._esperar(3)

    def carregar(self):
        emu.savestateload()

    def escolher_fase(self, fase):
        if fase is 1:
            joypad.write(1, controle_nes["esquerda"])
            time.sleep(0.01)
            joypad.write(1, controle_nes["cima"])
        elif fase is 2:
            joypad.write(1, controle_nes["cima"])
        elif fase is 3:
            joypad.write(1, controle_nes["direita"])
            time.sleep(0.01)
            joypad.write(1, controle_nes["cima"])
        elif fase is 4:
            joypad.write(1, controle_nes["esquerda"])
        elif fase is 5:
            joypad.write(1, controle_nes["direita"])
        elif fase is 6:
            joypad.write(1, controle_nes["esquerda"])
            time.sleep(0.01)
            joypad.write(1, controle_nes["baixo"])
        elif fase is 7:
            joypad.write(1, controle_nes["baixo"])
        elif fase is 8:
            joypad.write(1, controle_nes["direita"])
            time.sleep(0.01)
            joypad.write(1, controle_nes["baixo"])
        else:
            print("Fase %i não existe!" % fase)
            return
        joypad.write(1, controle_nes["A"])
        self._esperar(11)

    def _esperar(self, tempo):
        for i in range(10):
            if self.emulador.isAlive():
                sleep(tempo/10)
            else: break

    def jogar(self, exibir=False):
        pass
