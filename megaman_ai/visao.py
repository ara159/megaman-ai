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
            for imagem in (sprites[estado]["sprites"]+sprites[estado]["mascaras"]):
                if not os.path.isfile(imagem):
                    print("O arquivo %s não pode ser como sprite," % imagem, end="")
                    print("ele não existe. Ignorando.")
            else:
                self.sprites[estado] = {
                    "sprites": [],
                    "mascaras": []
                }

                for sprite in sprites[estado]["sprites"]:
                    imagem = cv2.imread(sprite, 1)
                    imagem = MegaMan.transformar(imagem)
                    self.sprites[estado]["sprites"].append(imagem)

                for mascara in sprites[estado]["mascaras"]:
                    imagem = cv2.imread(mascara, 0)
                    self.sprites[estado]["mascaras"].append(imagem)

    def atualizar(self, imagem):
        melhor  = 0
        estado  = None
        direcao = ""
        spriteMelhor = []

        for _estado in self.sprites:
            todos = self.sprites[_estado]["sprites"]

            for i in range(len(todos)):
                
                _sprite = self.sprites[_estado]["sprites"][i]
                _mask   = self.sprites[_estado]["mascaras"][i]
            
                for _direcao in ["direita", "esquerda"]:
                    if _direcao == "esquerda":

                        _sprite = cv2.flip(_sprite, 1)
                        _mask   = cv2.flip(_mask, 1)

                    encontrado  = cv2.matchTemplate(imagem, _sprite, cv2.TM_CCORR_NORMED, None, _mask)
                    status      = cv2.minMaxLoc(encontrado)
                    
                    if status[1] > melhor:
                        melhor  = status[1]
                        estado  = _estado
                        direcao = _direcao
                        spriteMelhor = _sprite
        else:
            self.estado = (estado, direcao)

        return melhor, spriteMelhor

    @staticmethod
    def transformar(imagem):
        # TODO: Continuar calibrar a transforamação para
        #       resultados melhores
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        # imagem = cv2.threshold(imagem, 70, 255, cv2.THRESH_BINARY)
        return imagem

    @staticmethod
    def combinarFundo(imagem, sprite):
        fundo = imagem[82:142, 98:158]
        largura = len(sprite[0])
        altura = len(sprite)
        fundo[0:altura, 0:largura] = sprite
        return fundo
           

    