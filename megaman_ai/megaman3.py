from time import sleep
import megaman_ai

class MegaMan3:
    def __init__(self, emulador):
        self.emulador = emulador
        self.controle = megaman_ai.emulador.Controle(emulador)

    def iniciar(self):
        self._esperar(6)
        self.controle.pausar()
        self._esperar(3)

    def carregar(self):
        sleep(0.3)
        self.controle._click(self.controle.carregar)

    def escolher_fase(self, fase):
        if fase is 1:
            self.controle.andar_esquerda(True)
            self.controle.subir(True)
        elif fase is 2:
            self.controle.subir(True)
        elif fase is 3:
            self.controle.andar_direita(True)
            self.controle.subir(True)
        elif fase is 4:
            self.controle.andar_esquerda(True)
        elif fase is 5:
            self.controle.andar_direita(True)
        elif fase is 6:
            self.controle.andar_esquerda(True)
            self.controle.descer(True)
        elif fase is 7:
            self.controle.descer(True)
        elif fase is 8:
            self.controle.andar_direita(True)
            self.controle.descer(True)
        else:
            print("Fase %i não existe!" % fase)
            return

        self.controle.pular(True)
        self.controle.soltar_controle()

        self._esperar(11)

    def _esperar(self, tempo):
        for i in range(10):
            if self.emulador.isAlive():
                sleep(tempo/10)
            else: break

    def jogar(self, exibir=False):
        pass
