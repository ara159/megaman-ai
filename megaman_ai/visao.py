import cv2
import mss
import numpy
import os

class MegaMan:
    sprites = {}
    frame   = False
    estado  = None
    direcao = 0
    posicao = None
    
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

    def atualizar(self, imagem, threashold):
        melhor  = 100
        estado  = None
        posicao = None
        direcao = ""

        for _estado in self.sprites:
            todos = self.sprites[_estado]["sprites"]

            for i in range(len(todos)):
                
                _sprite = self.sprites[_estado]["sprites"][i]
                _mask   = self.sprites[_estado]["mascaras"][i]
            
                for _direcao in ["direita", "esquerda"]:
                    if _direcao == "esquerda":

                        _sprite = cv2.flip(_sprite, 1)
                        _mask   = cv2.flip(_mask, 1)

                    encontrado  = cv2.matchTemplate(imagem, _sprite, cv2.TM_SQDIFF, None, _mask)
                    status      = cv2.minMaxLoc(encontrado)

                    if status[0] < melhor:
                        melhor  = status[0]
                        estado  = _estado
                        direcao = _direcao
                        posicao = status[2]

        else:
            if melhor <= threashold:
                self.estado = [estado, direcao]
                self.posicao = posicao
            else:
                self.estado = [None, None]
                self.posicao = None

        return melhor
    
    def desenhar_infos(self, frame, progresso, qualidade):
        try:
            tl = (self.posicao[0], self.posicao[1])
            br = (tl[0]+20, tl[1]+23)
            cv2.rectangle(frame, tl, br, (255,255,255), 1)
        except: 
            pass
        frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
        estado = "Estado: "+str(self.estado[0])+"+"+str(self.estado[1])
        qualidade = "Qualidade: "+str(100-qualidade)+"%"
        progresso = "Progresso: "+str(progresso)+"%"
        cv2.rectangle(frame, (70, 0), (390, 75), (0,0,0), -1)
        cv2.putText(frame, estado, (80,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.putText(frame, qualidade, (80,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.putText(frame, progresso, (80,60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.imshow("Megama-AI - Estados", frame)
        
    @staticmethod
    def transformar(imagem):
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        imagem = cv2.threshold(imagem, 70, 255, cv2.THRESH_BINARY)[1]
        return imagem
