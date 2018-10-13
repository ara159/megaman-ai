import mss
import cv2
import numpy

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
lhp = ((32,31), (44,142)) # ponto superior esquerdo, ponto inferior direito (x,y)
HP_MIN = 122 # Quando o HP está vazio, ainda ficam HP_MIN pixels brancos
HP_MAX = 727 # Quando o HP está cheio, ainda ficam HP_MIN pixels brancos
HP_TOT = HP_MAX - HP_MIN # Quantidade de pixels que indicam a vida atual

#Modos de exibição
COLORIDO = 0
THRESHOLD = 1

# Modo de exibição inicial
MODO_EXIB = 0

with mss.mss() as cpt:
    while "Olhando o jogo":
        # Tranforma a imagem da tela em um array numpy
        img = numpy.array(cpt.grab(JANELA_CAPTURA))
        
        # Contorna a região do hp na imagem
        cv2.rectangle(img, lhp[0], lhp[1], (255,255,255), 1)
        
        # Converte a imagem para preto e branco
        pb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Aplica um threshold que transforma pixels > 255 e < 120 em pretos
        th = cv2.threshold(pb, 120, 255, cv2.THRESH_BINARY)[1]
        
        # Pega somente a parte da tela que exibe o HP
        hp = th[lhp[0][1]:lhp[1][1],lhp[0][0]:lhp[1][0]]
        
        # Calculo a vida restante fazendo uma contagem de pixels brancos
        # e fazendo uma porcentagem do que ainda tem em ralação ao total
        vida = int((((hp == 255).sum() - HP_MIN) / (HP_TOT)) * 100)
        
        # Escreve na imagem o HP
        cv2.putText(img, str(vida)+"%", (30, 30), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)
        
        # Escolhe o modo de exibição
        # Serve para debugar talvez, ou perceber a diferença de interpretação
        # da máquina com o valor real
        # 'q' encerra o programa
        # 'w' muda para colorido
        # 'e' muda para threshould
        if cv2.waitKey(1) & 0xFF == ord("w"):
            MODO_EXIB = COLORIDO
        elif cv2.waitKey(1) & 0xFF == ord("e"):
            MODO_EXIB = THRESHOLD
        elif cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
        
        # Exibe a janela do game
        if MODO_EXIB == COLORIDO:
            cv2.imshow("Megaman-CV", img)
        elif MODO_EXIB == THRESHOLD:
            cv2.imshow("Megaman-CV", th)