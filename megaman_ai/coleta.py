import mss
import cv2
import numpy
import timeit
import time
import yaml
import os
from megaman_ai import visao, config

def quant_sprites(sprites):
    soma = 0
    for estado in sprites: 
        soma += len(sprites[estado])
    return soma * 2

def capturar(capturador, janela):
    image = numpy.array(capturador.grab(janela))
    return image

def iniciar(videos,
            skip_to    = 0,
            exibir     = False,
            estats_temp= False):

    megaman   = visao.MegaMan(sprites=config.sprites)
    
    if not len(videos):
        print("Nenhum video passado!")
        return

    for video in videos:
        if os.path.isfile(video):
            if not video[-3:] in ("mp4"):
                print(video, "Formato incompativel.")
                return

        video_nome = video.split("/")[-1][:-4]
        cap = cv2.VideoCapture(video)
            
        if not cap.set(cv2.CAP_PROP_POS_FRAMES, skip_to):
            print("Não foi possível skipar o video para o frame %d" % skip_to)
            return

        print("** Video %s **" % video_nome)
        print("** Configurações de coleta **")
        print("Frames por segundo Original: %d" % cap.get(cv2.CAP_PROP_FPS))
        print("Frame inicial: %d" % skip_to)
        print("Tempo inicial: %d" % (cap.get(cv2.CAP_PROP_POS_MSEC)/1000))
        print("Altura do frame Original: %d" % cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print("Largura do frame original: %d" % cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        print("Quantidade de sprites de personagem: %d" % quant_sprites(config.sprites))
        print("")
        
        tpasta = "treinamento/"+video_nome
        
        if not os.path.exists(tpasta):
            os.mkdir(tpasta)
            
        dados = open(tpasta+"/estados.yaml", "w")
        frame_anter = None

        try:
            while cap.isOpened():
                
                frame_num = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

                # imprime informações sobre o tempo
                if estats_temp:
                    print("Tempo : %fs" % (cap.get(cv2.CAP_PROP_POS_MSEC)/1000), end=" ")
                    print("Frame : %d" % frame_num)

                try:
                    frame_c = cv2.resize(cap.read()[1], (256,240))
                except:
                    print("Fim de video.")
                    break

                frame = visao.MegaMan.transformar(frame_c)
                melhor = megaman.atualizar(frame, 20)
                dados.write(yaml.dump({frame_num: megaman.estado}, default_flow_style=False))
                
                if not frame_anter is None:
                    cv2.imwrite(tpasta+"/"+str(frame_num)+".jpg", frame_anter)

                print("Qualidade:", str(melhor), end=", ")
                print("Estado:", megaman.estado)
                
                frame_anter = frame

                # imprime saida visual
                if exibir:
                    e = cv2.resize(frame_c, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
                    megaman.desenhar_infos(e)
                    cv2.imshow("Megama-AI - Estados", e)
                    if (cv2.waitKey(1) & 0xFF) == ord("q"):
                        cv2.destroyAllWindows()
                        break
        
        except KeyboardInterrupt as erro:
            dados.close()
            print("Coleta iterrompida pelo usuário.")
            return

    dados.close()
    print("Coleta finalizada!")