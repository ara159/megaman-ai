import mss
import cv2
import numpy
import timeit
import time
from megaman_ai import visao

def quant_sprites(sprites):
    soma = 0
    for estado in sprites: 
        soma += len(sprites[estado])
    return soma * 2

def capturar(cap, janela):
    image = numpy.array(cap.grab(janela))
    return image

def iniciar(config, 
            frames_seg = 30,
            exibir     = False,
            estats_temp= False):

    captura       = mss.mss()
    megaman       = visao.MegaMan(sprites=config.sprites)
    seg_frame     = 1/frames_seg
    tempo_passado = 0

    print("FPS    : %d" % frames_seg)
    print("Sprites: %d" % quant_sprites(config.sprites))

    while True:
        tempo_inicio = timeit.default_timer()
        
        imagem = capturar(captura, config.video)
        imagem = visao.MegaMan.transformar(imagem)

        melhor = megaman.atualizar(imagem)

        if melhor < 1:
            print("Qualidade:"+str(int(100-(melhor*100)))+"%", end=", ")
            print("Estado:", megaman.estado)
        else:
            print("---")     
               
        if exibir:
            cv2.imshow("Coleta", imagem)
            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                cv2.destroyAllWindows()
                break

        tempo_passado = timeit.default_timer() - tempo_inicio
        tempo_sobra   = seg_frame - tempo_passado
        
        if estats_temp:
            print("Tempo de execução do frame: ", tempo_passado)
        
        if tempo_sobra > 0: 
            time.sleep(tempo_sobra)
