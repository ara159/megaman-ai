from megamanAI import emulador
from time import sleep

from megamanAI.emulador import Controle
from megamanAI.visao import *

class MegaMan3:
    def __init__(self, emulador):
        self.emulador = emulador
        self.controle = Controle(emulador)

    def iniciar(self, carregar=True):
        if carregar:
            sleep(1)
            self.controle._click(self.controle.carregar)
        else:
            self._esperar(6)
            self.controle.pausar()
            self._esperar(3)

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

    def jogar(self):
        p_janela = {
            "top": 25+self.emulador.posicao[1],
            "left": 2+self.emulador.posicao[0],
            "width": 256*self.emulador.escala,
            "height": 224*self.emulador.escala
        }

        mm = MegaMan({
            "parado": "sprites/sprite_megaman_parado.png",
            "correndo_1": "sprites/sprite_megaman_correndo1.png",
        })

        hp = HP(Ponto(24, 16), Ponto(31, 72))
        cn = Cenario()

        capture = mss.mss()

        while "Olhando tela":
            img = numpy.array(capture.grab(p_janela))
            pb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # th = cv2.threshold(pb, 120, 255, cv2.THRESH_BINARY)[1]

            mm.atualizar(pb)
            hp.atualizar(pb)

            if cn.solo is None:
                cn.solo = pb[mm.p2.y+1:mm.p2.y+5, mm.p1.x-2:mm.p2.x+2]

            mm.pintar(img)
            hp.pintar(img)
            # cn.pintar_solo(pb, img)

            cv2.imshow("megaman-cv", img)

            if cv2.waitKey(1) and not self.emulador.isAlive():
                cv2.destroyAllWindows()
                break
