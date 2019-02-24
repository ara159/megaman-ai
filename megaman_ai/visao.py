import cv2
import mss
import numpy
import os

class MegaMan:
    sprites = {}
    frame   = False
    estado  = None
    direcao = 0
    
    def __init__(self, sprites):
        for estado in sprites:
            for sprite in sprites[estado]:
                if not os.path.isfile(sprite):
                    print("O arquivo %s não pode ser como sprite," % sprite, end="")
                    print("ele não existe. Ignorando.")
            else:
                self.sprites[estado] = []
                for sprite in sprites[estado]:
                    imagem = cv2.imread(sprite)
                    imagem = MegaMan.transformar(imagem)
                    self.sprites[estado].append(imagem)

    def atualizar(self, imagem):
        melhor  = 1
        estado  = None
        direcao = ""
        for _estado in self.sprites:
            todos = self.sprites[_estado]
            for _sprite in todos:
                for _direcao in ["direita", "esquerda"]:
                    if _direcao == "esquerda":
                        _sprite = cv2.flip(_sprite, 0)
                    encontrado  = cv2.matchTemplate(imagem, _sprite, cv2.TM_SQDIFF_NORMED,)
                    status      = cv2.minMaxLoc(encontrado)
                    if status[0] < melhor:
                        melhor  = status[0]
                        estado  = _estado
                        direcao = _direcao
        else:
            self.estado  = (estado, direcao)

        return melhor

    @staticmethod
    def transformar(imagem):
        # TODO: Continuar calibrar a transforamação para
        #       resultados melhores
        
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        # blur
        # imagem      = cv2.blur(imagem, (1,1))
        # imagem      = cv2.medianBlur(imagem, 1)
        
        # threshold
        imagem = cv2.threshold(imagem,80,100,cv2.THRESH_BINARY)[1]
        # imagem      = cv2.Canny(imagem, 80, 100)
        # imagem = cv2.GaussianBlur(imagem,(3,3),0)
        return imagem