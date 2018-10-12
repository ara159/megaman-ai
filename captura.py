import mss
import cv2
import numpy

# Tamanho da sua tela
TELA_LARGURA = 1366
TELA_ALTURA = 768

# Tamanho da tela do jogo
# Obs: Com ela já na posição inferior esquerda
# ----------------------
# -         |          -
# -         |          -
# ----------------------
# -XXXXXXXXX|          -
# -XXXXXXXXX|          -
# ----------------------
GAME_LARGURA = 497
GAME_ALTURA = 448

JANELA_CAPTURA = {
    "top": 290,
    "left": 17, 
    "width": GAME_LARGURA, 
    "height": GAME_ALTURA
}
# Limites do HP - Retangulo
lhp = ((32,31), (44,142))
HP_MIN = 122
HP_MAX = 727

with mss.mss() as cpt:
    while "Capturando Tela":
        img = numpy.array(cpt.grab(JANELA_CAPTURA))
        # cv2.rectangle(img, (42,142), (34,34), (255,0,0), 2)
        cv2.rectangle(img, lhp[0], lhp[1], (255,255,255), 1)
        pb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        th = cv2.threshold(pb, 120, 255, cv2.THRESH_BINARY)[1]
        hp = th[lhp[0][1]:lhp[1][1],lhp[0][0]:lhp[1][0]]
        # saida = numpy.hstack((pb[::,:int(GAME_LARGURA/2)], th[::,int(GAME_LARGURA/2):]))

        vida = int((((hp == 255).sum()-HP_MIN)/(HP_MAX-HP_MIN))*100)
        cv2.putText(img,str(vida)+"%",(30, 30), cv2.FONT_HERSHEY_PLAIN, 1,(255,255,255),1)

        cv2.imshow("Game", img)
        
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break