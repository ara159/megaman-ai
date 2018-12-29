import cv2
import mss
import numpy

class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def tupla(self):
        return (self.x, self.y)
    
    def __repr__(self):
        return "Ponto("+str(self.x)+", "+str(self.y)+")"

class Retangulo:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def pintar(self, img, cor=(255, 255, 255), grossura=1):
        cv2.rectangle(img, self.p1.tupla(), self.p2.tupla(), cor, grossura)
    
    def centro(self):
        return Ponto(self.p1.x+int((self.p2.x-self.p1.x)/2), self.p1.y+int((self.p2.y-self.p1.y)/2))

class Cenario:
    solo = None # sprite

    def pintar_solo(self, pb, img, cor=(0, 255, 0), grossura=1):
        larg, alt = self.solo.shape[::-1]
        result = cv2.matchTemplate(pb, self.solo, cv2.TM_CCOEFF_NORMED)
        loc = numpy.where(result > 0.5)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0]+larg, pt[1]+alt), cor, grossura)

class HP(Retangulo):
    maximo = 122
    atual = 0

    def __init__(self, p1, p2):
        super(HP, self).__init__(p1, p2)

    def atualizar(self, img_pb):
        corte = img_pb[self.p1.y:self.p2.y, self.p1.x:self.p2.x]
        self.atual = (corte == 224).sum()

class MegaMan(Retangulo):
    sprites = {}
    direcao = 0
    in_frame = False

    def __init__(self, sprites):
        super(MegaMan, self).__init__(Ponto(0,0), Ponto(0,0))
        for estado in sprites:
            self.sprites[estado] = cv2.imread(sprites[estado], 0)
        self.direcao = 0
        self.tam_janela = 20

    def janela(self, img):
        if self.in_frame:
            if self.p1.x > self.tam_janela+1 and self.p2.x < 256-self.tam_janela:
                return img[self.p1.y-self.tam_janela:self.p2.y+self.tam_janela, self.p1.x-self.tam_janela:self.p2.x+self.tam_janela]
        return img

    def atualizar(self, img):
        for estado in self.sprites:
            result = cv2.matchTemplate(self.janela(img), self.sprites[estado], cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if min_val < 0.1:
                w, h = self.sprites[estado].shape[::-1]
                anter = self.in_frame
                self.in_frame = True
                
                if anter:
                    self.p1 = Ponto(self.p1.x+min_loc[0]-20, self.p1.y+min_loc[1]-20)
                    self.p2 = Ponto(self.p1.x+w, self.p1.y+h)
                else:
                    self.p1 = Ponto(min_loc[0], min_loc[1])
                    self.p2 = Ponto(self.p1.x+w, self.p1.y+h)
                
                # break
        # else:
        #     print("Não aparece no frame")
        #     self.in_frame = False

    def pintar(self, img):
        super(MegaMan, self).pintar(img)
        cv2.rectangle(img, (self.p1.x-20, self.p1.y-20), (self.p2.x+20, self.p2.y+20), (255, 0, 0), 1)


def jogar_fase(emu):
    p_janela = {
        "top": 25+emu.posicao[1],
        "left": 2+emu.posicao[0],
        "width": 256*emu.escala,
        "height": 224*emu.escala
    }
    
    mm = MegaMan({
        "parado": "sprites/sprite_megaman_parado.png",
        "correndo_1": "sprites/sprite_megaman_correndo1.png",
        "correndo_2": "sprites/sprite_megaman_correndo2.png",
        "correndo_3": "sprites/sprite_megaman_correndo3.png",
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

        if cv2.waitKey(1) and not emu.isAlive():
            cv2.destroyAllWindows()
            break

            cv2.dis
