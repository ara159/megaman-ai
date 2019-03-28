import mss
import cv2
import numpy
import timeit
import time
from megaman_ai import visao, config

def quant_sprites(sprites):
    soma = 0
    for estado in sprites: 
        soma += len(sprites[estado])
    return soma * 2

def capturar(capturador, janela):
    image = numpy.array(capturador.grab(janela))
    return image

def iniciar(skip_to    = 0,
            exibir     = False,
            estats_temp= False):

    megaman   = visao.MegaMan(sprites=config.sprites)
    cap       = cv2.VideoCapture("/home/rafael/megaman-ai/gameplay_no_damage.mp4")
    
    if not cap.set(cv2.CAP_PROP_POS_FRAMES, skip_to):
        print("Não foi possível skipar o video para o frame %d" % skip_to)
        return

    print("** Configurações de coleta **")
    print("Frames por segundo Original: %d" % cap.get(cv2.CAP_PROP_FPS))
    print("Frame inicial: %d" % skip_to)
    print("Tempo inicial: %d" % (cap.get(cv2.CAP_PROP_POS_MSEC)/1000))
    print("Altura do frame Original: %d" % cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Largura do frame original: %d" % cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("Quantidade de sprites de personagem: %d" % quant_sprites(config.sprites))
    print("")

    ultimo_estado = None
    ultimo_frame  = None
    image_nome    = 0

    while cap.isOpened():
        # imprime informações sobre o tempo
        if estats_temp:
            print("Tempo : %fs" % (cap.get(cv2.CAP_PROP_POS_MSEC)/1000), end=" ")
            print("Frame : %d" % int(cap.get(cv2.CAP_PROP_POS_FRAMES)))

        frame     = cv2.resize(cap.read()[1], (256,240))
        frame_pb  = visao.MegaMan.transformar(frame)
        melhor    = megaman.atualizar(frame_pb)
        
        if megaman.estado != ultimo_estado:
            if ultimo_estado != None:
                print("Transição:", ultimo_estado[0], megaman.estado[0])
            ultimo_estado = megaman.estado
            ultimo_frame  = frame

        # # imprime informações sobre a qualidade
        if melhor <= 20:
            print("Qualidade:", str(melhor), end=", ")
            print("Estado:", megaman.estado)
        else:
            print("---")
        
        # imprime saida visual
        if exibir:
            rframe = cv2.resize(frame, None, fx=2, fy=2)
            megaman.desenhar_infos(rframe)
            cv2.imshow("Megama-AI", rframe)
            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                cv2.destroyAllWindows()
                break