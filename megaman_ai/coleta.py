import cv2
import numpy
import yaml
import os
from megaman_ai import visao, config

def iniciar(videos, skip_to=0, exibir=False, estats_temp=False):
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
        tpasta = "treinamento/"+video_nome
        dataset = tpasta+"/estados.yaml"

        # verifica se precisa criar a pasta
        if not os.path.exists(tpasta):
            os.mkdir(tpasta)
        
        # verifica se da para continuar de onde parou
        if os.path.exists(dataset):
            arq = open(dataset, "r")
            yml = yaml.load(arq.read())
            skip_to = list(yml.keys())[-1]+1
            print("** Continuando "+video_nome+"**")
        
        # inicia o leitor de video
        cap = cv2.VideoCapture(video)
        
        # verifica se o video já foi feito até o fim, se foi vai para o proximo video
        if skip_to == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            print(video, " feito!")
            continue
        
        # tenta eskipar o video para o ultimo frame, ou um recebido por param
        if not cap.set(cv2.CAP_PROP_POS_FRAMES, skip_to):
            print("Não foi possível skipar o video para o frame %d" % skip_to)
            return
        
        # exibe algumas informações sobre o video e o procedimento
        print("** Video %s **" % video_nome)
        print("** Configurações de coleta **")
        print("Frames por segundo Original: %d" % cap.get(cv2.CAP_PROP_FPS))
        print("Frame inicial: %d" % skip_to)
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
                if (not frame_anter is None) and estats_temp:
                    print("Tempo : %fs" % (cap.get(cv2.CAP_PROP_POS_MSEC)/1000))
                    print("Frame : %d" % frame_num)

                # obtém o frame e tenta redimencionar, pode falhar se já está no fim do video
                try:
                    frame_c = cv2.resize(cap.read()[1], (256,240))
                except:
                    print("Fim de video. O arquivo contém informações de todos os frames.")
                    break

                # aplica as tranformações necessárias
                frame = visao.MegaMan.transformar(frame_c)
                # atualizar o estado do objeto megaman usando o frame
                melhor = megaman.atualizar(frame, 20)
                # armazena o numero do frame atual com o estado atual no dataset
                dados.write(yaml.dump({frame_num: megaman.estado}, default_flow_style=False))
                
                # armazena o frame anterior com o numero do frame_atual.
                # ou seja, na leitura, a imagem será do frame anterior, e o estado do frame atual
                # já estará pronto para o treino do classificador
                if not frame_anter is None:
                    cv2.imwrite(tpasta+"/"+str(frame_num)+".jpg", frame_anter)

                # atualiza o frame anterior
                frame_anter = frame

                # imprime informações de qualidade e estados para cada frame
                print("Qualidade:", str(100-melhor)+"%")
                print("Estado:", megaman.estado)
                
                progresso = int((frame_num/frames_tot)*100)
                print("Progresso: ["+"#"*int(progresso/4)+">"+"."*(int(100/4)-int(progresso/4))+"]", str(progresso)+"%")
                
                # imprime saida visual
                if exibir:
                    e = cv2.resize(frame_c, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
                    megaman.desenhar_infos(e)
                    cv2.imshow("Megama-AI - Estados", e)
                    if (cv2.waitKey(1) & 0xFF) == ord("q"):
                        cv2.destroyAllWindows()
                        break
        
        # ser iterrompido pelo teclado
        except KeyboardInterrupt:
            dados.close()
            print("Coleta iterrompida pelo usuário.")
            return

        # finalizado por exaustão
        dados.close()
        print("Coleta finalizada!")