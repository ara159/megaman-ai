import cv2
import numpy
import os

class MegaMan:
    sprites = {}
    frame   = False
    estado  = None
    direcao = 0
    posicao = None
    sobra   = 20
    
    def __init__(self, sprites):
        pastaSprite = sprites["sprites"]
        pastaMascara = sprites["mascaras"]
        extencao = sprites["extencao"]
        estados = sprites["estados"]

        # abre os sprites e máscaras
        for estado in estados:
            novoEstado = {"sprites": [], "mascaras": []}
            for arquivo in estados[estado]:
                sprite = cv2.imread("{}/{}.{}".format(pastaSprite, arquivo, extencao), 1)
                novoEstado["sprites"].append(MegaMan.transformar(sprite))
                mascara = cv2.imread("{}/{}.{}".format(pastaMascara, arquivo, extencao), 0)
                novoEstado["mascaras"].append(mascara)
            self.sprites[estado] = novoEstado
        
        # rótulos
        self.rotulos = self.sprites.keys()

    def janela(self, imagem):
        if self.posicao != None:
            x, y = self.posicao
            descy = y + 31 + self.sobra
            descx = x + 25 + self.sobra
            if y > self.sobra and x > self.sobra and \
                    descy < imagem.shape[0] and descx < imagem.shape[1]:
                return imagem[y-self.sobra:descy, x-self.sobra:descx]
            else:
                self.posicao = None
        return imagem

    def atualizar(self, imagem, threashold):
        melhor  = 100
        estado  = None
        posicao = None
        direcao = ""
        janela = self.janela(imagem)

        for _estado in self.sprites:
            todos = self.sprites[_estado]["sprites"]

            for i in range(len(todos)):
                
                _sprite = self.sprites[_estado]["sprites"][i]
                _mask   = self.sprites[_estado]["mascaras"][i]
            
                for _direcao in ["direita", "esquerda"]:
                    if _direcao == "esquerda":

                        _sprite = cv2.flip(_sprite, 1)
                        _mask   = cv2.flip(_mask, 1)

                    encontrado  = cv2.matchTemplate(janela, _sprite, cv2.TM_SQDIFF, None, _mask)
                    status      = cv2.minMaxLoc(encontrado)

                    if status[0] < melhor:
                        melhor  = status[0]
                        estado  = _estado
                        direcao = _direcao
                        posicao = status[2]
        else:
            if melhor <= threashold:
                self.estado = [estado, direcao]
                if self.posicao == None:
                    self.posicao = posicao
                else:
                    self.posicao = (self.posicao[0]-self.sobra+posicao[0], self.posicao[1]-self.sobra+posicao[1]) 
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
