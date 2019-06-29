import cv2
import numpy
import yaml
import os
from megaman_ai import visao, config

def iniciar(videos, pasta_dest="", frame_inicial=0, exib_video=False, exib_tempo=False, exib_qualidade=False):
    # cria um auxiliar para a visão computacional
    megaman   = visao.MegaMan(sprites=config.sprites)
    
    # testa se os videos passados existem
    if not len(videos):
        print("Nenhum video passado!")
        return

    # inicia para um video de cada vez
    for video in videos:

        # testa se os videos existem e estão em um formato compativel
        if os.path.isfile(video):
            if not video[-3:] in ("mp4"):
                print(video, "Formato incompativel.")
                return
        else:
            print(video, "Não existe.")
            return

        # seta o caminho para os arquivos gerados
        video_nome = video.split("/")[-1][:-4]
        tpasta = pasta_dest+video_nome
        dataset = tpasta+"/estados.yaml"
    
        # verifica se precisa criar a pasta
        if not os.path.exists(tpasta):
            os.mkdir(tpasta)
        
        # verifica se da para continuar de onde parou
        if os.path.exists(dataset):
            arq = open(dataset, "r")
            yml = yaml.load(arq.read())
            frame_inicial = list(yml.keys())[-1]+1
            print("** Continuando "+video_nome+"**")
        
        # inicia o leitor de video
        cap = cv2.VideoCapture(video)
        
        # verifica se o video já foi feito até o fim, se foi vai para o proximo video
        if frame_inicial == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            print("%s já foi routulado completamente!" % video)
            continue
        
        # tenta eskipar o video para o ultimo frame, ou um recebido por param
        if not cap.set(cv2.CAP_PROP_POS_FRAMES, frame_inicial):
            print("Não foi possível skipar o video para o frame %d" % frame_inicial)
            return
        
        # exibe algumas informações sobre o video e o procedimento
        print("** Video %s **" % video_nome)
        print("** Configurações de coleta **")
        print("Frames por segundo Original: %d" % cap.get(cv2.CAP_PROP_FPS))
        print("Frame inicial: %d" % frame_inicial)
        print("Tempo inicial: %d" % (cap.get(cv2.CAP_PROP_POS_MSEC)/1000))
        print("Altura do frame Original: %d" % cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print("Largura do frame original: %d" % cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        print("")
        
        # abre o arquivo de dataset
        dados = open(dataset, "a")
        
        # o frame_anter armazena o frame anterior
        frame_anter = None

        frames_tot = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        # inicia o procedimento
        try:
            while cap.isOpened():
                # obtem o numero do próximo frame a ser lido
                frame_num = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

                # imprime informações sobre o tempo se solicitado
                if (not frame_anter is None) and exib_tempo:
                    print("Tempo : %fs" % (cap.get(cv2.CAP_PROP_POS_MSEC)/1000))
                    print("Frame : %d" % frame_num)

                # obtém o frame e tenta redimencionar, pode falhar se já está no fim do video
                try:
                    frame_c = cv2.resize(cap.read()[1], (256,240))
                except:
                    print("Fim de video. Rotulação completa do video %s" % video)
                    print("Pasta com os arquivos: %s" % tpasta)
                    break

                # aplica as tranformações necessárias
                frame = visao.MegaMan.transformar(frame_c)
                # atualizar o estado do objeto megaman usando o frame
                melhor = megaman.atualizar(frame, 20)
                
                # armazena o frame anterior com o numero do frame_atual.
                # ou seja, na leitura, a imagem será do frame anterior, e o estado do frame atual
                # já estará pronto para o treino do classificador
                # armazena o numero do frame atual com o estado atual no dataset
                if not frame_anter is None:
                    dados.write(yaml.dump({frame_num: megaman.estado}, default_flow_style=False))
                    cv2.imwrite(tpasta+"/"+str(frame_num)+".jpg", frame_anter)

                # atualiza o frame anterior
                frame_anter = frame_c

                # imprime informações de qualidade e estados para cada frame
                if exib_qualidade:
                    print("Qualidade:", str(100-melhor)+"%")
                    print("Estado:", megaman.estado)
                
                progresso = int((frame_num/frames_tot)*100)
                print("\rProgresso: ["+"#"*int(progresso/4)+">"+"."*(int(100/4)-int(progresso/4))+"]", str(progresso)+"%\r", end="")
                
                # imprime saida visual
                if exib_video:
                    megaman.desenhar_infos(frame_c, progresso, melhor)
                    if (cv2.waitKey(1) & 0xFF) == ord("q"):
                        print("")
                        print("Coleta finalizada pelo usuário.")
                        break

        # ser iterrompido pelo teclado
        except KeyboardInterrupt:
            dados.close()
            print("")
            print("Coleta iterrompida pelo usuário.")
            return
        
        cv2.destroyAllWindows()
        dados.close()