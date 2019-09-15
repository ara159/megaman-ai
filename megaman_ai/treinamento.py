""" 
treinamento.py
Classes de execução do treinamento da rede neural a partir dos videos.
"""

# * Treinando frame a frame
# TODO: A contagem das estatísticas estão erradas. Consertar.

import cv2
import numpy
import yaml
import os
import time
from datetime import datetime
from threading import RLock, Thread, active_count
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator

from . import inteligencia, visao

class Treinamento:
    """Armazena informações sobre uma instancia de treinamento
    incluindo estatísticas sobre o andamento do treinamento."""

    def __init__(self, videos, sprites, **kwargs):
        self.videos = videos
        self.visao = visao.MegaMan(sprites)
        self.tempo = kwargs.get("tempo", False)
        self.exibir = kwargs.get("exibir", False)
        self.qualidade = kwargs.get("qualidade", False)
        self.epochs = kwargs.get("epochs", 50)
        self.batch_size = kwargs.get("batch_size", 100)
        self.nome = kwargs.pop("nome")
        self.sprites = sprites
        self._suffle = not kwargs.get("not_suffle", False)
        self._fimVideo = False
        self._nthreads = kwargs.get("nthreads", 4)
        self._frameAnterior = None, -1
        self._s = [],[]
        self._log = open("logs/"+self.nome+".log", "a")
        self._lock = RLock()
        self._rnn = True

    def iniciar(self):
        """Inicia o treinamento em todos os videos"""
        
        self._exibirInfoInicioTreino()

        for video in self.videos:

            # Abre o video
            videoCapture = cv2.VideoCapture(video)

            # Exibe algumas informações antes do inicio do treinamento
            self._exibirInfosInicioVideo(video)

            try:
                # Chama a função de treinamento para o video atual
                self._treinar(videoCapture)
                print("\n")
            # Trata o caso de iterrupção pelo usuário via teclado
            # Para salvar o progresso do video
            except KeyboardInterrupt:
                print("Iterrompido pelo usuário.")
                

            # Exibe informações no fim do treinamento
            self._exibirInfosFimVideo(video)
            
            # Salva modelo
            inteligencia.salvar()
        
        self._exibirInfoFimTreino()

    def _exibirInfosFimVideo(self, video):
        """Exibe algumas informações antes do treinamento com o video"""
        print("Fim de treinamento com o vídeo: {}".format(video))

    def _exibirInfosInicioVideo(self, video):
        """Exibe algumas informações depois do treinamento com o video"""
        print("Iniciando Treino: {}".format(video))

    def _exibirInfoInicioTreino(self):
        print("""
  __  __                  __  __                  _    ___ 
 |  \/  | ___  __ _  __ _|  \/  | __ _ _ __      / \  |_ _|
 | |\/| |/ _ \/ _` |/ _` | |\/| |/ _` | '_ \    / _ \  | | 
 | |  | |  __/ (_| | (_| | |  | | (_| | | | |  / ___ \ | | 
 |_|  |_|\___|\__, |\__,_|_|  |_|\__,_|_| |_| /_/   \_\___|
              |___/                                        
    
    Iniciando treinamento... 
    Videos: {}
    Batch Size: {}
    Epochs: {}
    """.format(self.videos, self.batch_size, self.epochs))

    def _exibirInfoFimTreino(self):
        print("""
Treinamento finalizado com sucesso!

Arquivo de log: "logs/{}.log"
Modelo: "{}"

Para jogar use o comando: 
    sudo python3 -m megaman_ai --nome={}
    """.format(self.nome, inteligencia._caminho, self.nome))
    
    def _iniciarClassificacao(self, videoCapture):
        temporario = []
        for i in range(self._nthreads):
            for _ in range(int(self.batch_size/self._nthreads)):
                frame = videoCapture.read()[1]
                if not frame is None:
                    temporario.append(frame)
                else:
                    self._fimVideo = True
                    break
            worker = Worker(temporario.copy(), self.sprites, self._s, self._lock)
            worker.start()
            print("Thread {} iniciada com {} frames".format(i+1, len(temporario)))
            temporario.clear()

    def _treinar(self, videoCapture):
        """Executa o treinamento em um video"""
        
        framesTotal = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
        feitos = 0

        # Lê o video até o fim
        while not self._fimVideo:
            
            self._iniciarClassificacao(videoCapture)

            while active_count() > 1:
                self._exibirInfoTreinamento(framesTotal, feitos)

            cv2.destroyAllWindows()

            if len(self._s[0]) > 0:
                if self._rnn:
                    self._fitRNN()
                else:
                    self._fit()
                feitos += len(self._s[0])
                # limpa o batch
                self._s[0].clear()
                self._s[1].clear()

    def _atualizarLog(self, historico):
        info = Info(
            acc = list(map(float, historico.history['acc'])), 
            loss = list(map(float, historico.history['loss'])),
            rotulos = self._s[1],
            tam_batch = len(self._s[0]))
        
        self._log.write(str(info))
        
    def _fit(self):
        treinar = True
        epochs = self.epochs
        ultimo = 0

        while treinar:
            historico = inteligencia.modelo.fit(
                numpy.array(self._s[0])/255.0, 
                numpy.array(self._s[1]),
                batch_size=self.batch_size,
                epochs=epochs, 
                verbose=1, 
                shuffle=self._suffle)

            self._atualizarLog(historico)
            
            atual = numpy.mean(historico.history["acc"])
            treinar = ((atual <= 0.80) or ((atual - ultimo) > 0.005))
            print("\033[31mVariação: ", (atual - ultimo), "\033[0;0m")
            ultimo = atual
    
    def _fitRNN(self):
        gerador = TimeseriesGenerator(
            numpy.array(self._s[0])/255.0, 
            numpy.array(self._s[1]), 
            length=20)
        historico = inteligencia.modelo.fit_generator(
            gerador,
            epochs=self.epochs,
            shuffle=self._suffle,
            verbose=1)
        self._atualizarLog(historico)
        
    def _exibirInfoTreinamento(self, total, feitos):
        """Print de informações sobre o andamento do treinamento"""
        # Progresso
        progresso = int(((len(self._s[0])+feitos)/total)*100)
        texto = "Progresso: [{}] {}% {}"
        statBatch = "{}/{}".format(len(self._s[0]), self.batch_size)
        preenchimento = "#"*int(progresso/4)+">"+"."*(int(100/4)-int(progresso/4))
        # imprime
        print(texto.format(preenchimento, progresso, statBatch), end="\r")
        # if self.exibir and len(self._s[0]) > 0:
        #     cv2.imshow("Treinamento", cv2.resize(self._s[0][-1], None, fx=8, fy=8, interpolation=cv2.INTER_NEAREST))
        #     cv2.waitKey(1)

class Info:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
    
    def __str__(self):
        return yaml.dump({datetime.now().isoformat(): self.__dict__})

class Worker(Thread):

    def __init__(self, frames, sprites, lista, lock, **kwargs):
        Thread.__init__(self)
        self.megaman = visao.MegaMan(sprites)
        self.frames = frames
        self.lista = lista
        self.lock = lock
        self.temporario = [],[]

    def run(self):
        frameAnterior = (None, -1)
        
        for frame in self.frames:
            
            frame = cv2.resize(frame, (256, 240))[:-16,:]
            
            # atualizar o estado do objeto megaman usando o frame
            self.megaman.atualizar(self.megaman.transformar(frame), 20)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            frame = cv2.resize(frame, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_NEAREST)
            
            # treina a rede com o frame anterior e o rótulo do frame atual
            # apenas nas transições
            temAnterior = not frameAnterior[0] is None
            isTransicao = True #frameAnterior[1] != self.megaman.rotulo # True
            temEstadoAtual = self.megaman.rotulo != -1
            excecao = self.megaman.rotulo in (10, 11)
            descSubida = False #self.megaman.rotulo in (8, 9) and frameAnterior[1] in (8, 9)  # False

            if temAnterior and isTransicao and temEstadoAtual and \
                not excecao and not descSubida:
                # coloca no dataset
                self.lock.acquire()
                self.lista[0].append(frameAnterior[0].flatten())
                self.lista[1].append(self.megaman.rotulo)
                self.lock.release()
            
            # atualiza o frame anterior
            frameAnterior = (frame, self.megaman.rotulo)
