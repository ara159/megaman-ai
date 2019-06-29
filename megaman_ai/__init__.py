import getopt

class Config:
    # Classe de configuração
    pass

config = Config()

from megaman_ai import emulador, coleta, megaman3
from server.rafael import *
import threading

def jogar(room, 
            sequencia  = [], 
            focar      = True, 
            foco_tx    = 0.3, 
            carregar   = False, 
            escala     = 1,
            exibir     = False):
    
    emu = emulador.Emulador(room=room)
    emu.start()
    print("Emulador iniciado")
    conectar()
    print("Conectado ao emulador")
    print("Fim Thread principal")
    return emu