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
GAME_LARGURA = 683
GAME_ALTURA = 513

JANELA_CAPTURA = {
    "top": TELA_ALTURA-GAME_ALTURA, 
    "left": 0, 
    "width": GAME_LARGURA, 
    "height": GAME_ALTURA
}

with mss.mss() as cpt:
    
    print("Para parar a captura, precione a tecla 'q'")

    while "Capturando Tela":
        img = numpy.array(cpt.grab(JANELA_CAPTURA))
        
        cv2.imshow("Imagem", img)
    
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break