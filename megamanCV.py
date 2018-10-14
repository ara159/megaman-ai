""" 
Megaman-CV

Execute:
    ./megamancv.sh [escala 1-4]
"""

import cv2
import mss
import numpy
from sys import argv

# Resolução do seu monitor
RESOLUCAO_MONITOR = [1366, 768]
# Escalo do game em relação ao original
GAME_ESCALA = int(argv[1])

# A resolução original do videogame NES - NÃO ALTERAR
RESOLUCAO_GAME = [256, 224]
# Resolução com a escala - NÃO ALTERAR
RESOLUCAO_GAME = [i * GAME_ESCALA for i in RESOLUCAO_GAME]

# Define a região do monitor a ser observada
JANELA_CAPTURA = {
    "top": RESOLUCAO_MONITOR[1] - RESOLUCAO_GAME[1], #290,
    "left": 0, #17, 
    "width": RESOLUCAO_GAME[0],
    "height": RESOLUCAO_GAME[1]
}

# Limites do HP - Retangulo
L_HP = ((25 * GAME_ESCALA, 17 * GAME_ESCALA), 
        (31 * GAME_ESCALA, 72 * GAME_ESCALA))
HP_MIN = 0 * GAME_ESCALA**2 # Quando o HP está vazio, ainda ficam HP_MIN pixels brancos
HP_MAX = 168 * GAME_ESCALA**2 # Quando o HP está cheio, ainda ficam HP_MIN pixels brancos
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

        # Converte a imagem para preto e branco
        pb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Aplica um threshold que transforma pixels > 255 e < 120 em pretos
        th = cv2.threshold(pb, 120, 255, cv2.THRESH_BINARY)[1]
        
        # Pega somente a parte da tela que exibe o HP
        hp = th[L_HP[0][1]:L_HP[1][1],L_HP[0][0]:L_HP[1][0]]
        
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
            cv2.rectangle(img, L_HP[0], L_HP[1], (255,255,255), 1)    
            cv2.imshow("MegamanCV", img)
        elif MODO_EXIB == THRESHOLD:
            cv2.rectangle(th, L_HP[0], L_HP[1], (255,255,255), 1)    
            cv2.imshow("MegamanCV", th)