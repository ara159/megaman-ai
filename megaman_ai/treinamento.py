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
from .comuns import sttinf, sttwrn

class Treinamento:
    """Armazena informações sobre uma instancia de treinamento
    incluindo estatísticas sobre o andamento do treinamento."""

    def __init__(self, videos, sprites, **kwargs):
        self.videos = videos
        self.visao = visao.MegaMan(sprites)
        self.epochs = kwargs.get("epochs", 50)
        self.batch_size = kwargs.get("batch_size", 100)
        self.frames = kwargs.get("frames", 1000)
        self.nome = kwargs.pop("nome")
        self.sprites = sprites
        self.suffle = kwargs.get("suffle", True)
        self.nthreads = kwargs.get("nthreads", 1)
        self.time_steps = kwargs.get("time_steps", 10)
        self._frameAnterior = None, -1
        self._data_set = [],[]
        self._log = open("logs/{}.log".format(self.nome), "a")
        self._rnn = True # Parametrizar
        self._iterativo = False # Parametrizar
        self._lock_video = RLock()
        self._frames_thread = int(self.frames/self.nthreads)

    def iniciar(self):
        """Inicia o treinamento em todos os videos"""
        
        self._exibirInfoInicioTreino()

        for video in self.videos:

            # Abre o video
            self._video = cv2.VideoCapture(video)

            # Exibe algumas informações antes do inicio do treinamento
            self._exibirInfosInicioVideo(video)

            try:
                # Chama a função de treinamento para o video atual
                self._treinar()
            
            # Trata o caso de iterrupção pelo usuário via teclado
            # Para salvar o progresso do video
            except KeyboardInterrupt:
                print(" "*150, end="\r")
                

            # Exibe informações no fim do treinamento
            self._exibirInfosFimVideo(video)
            
            # Salva modelo
            inteligencia.salvar()
        
    def _exibirInfosFimVideo(self, video):
        """Exibe algumas informações antes do treinamento com o video"""
        print("[{}] Fim de treinamento com o vídeo {}. Feitos: {}/{}".format(
                sttwrn, 
                video, 
                self.feitos, 
                self.framesTotal))

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
    
    Nome IA: {}
    Epochs: {}
    Batch Size: {}
    Threads: {}
    Frames/fit: {}
    Videos: {}
    """.format(self.nome, self.epochs, self.batch_size, 
        self.nthreads, self.frames, self.videos))
    
    def _iniciarClassificacao(self):
        frame_set = []
        feitos = 0
        threads = []

        print("[{}] Iniciando classificação".format(sttinf))

        for i in range(self.nthreads):
            recipiente = [],[]
            frame_set.append(recipiente)
            args = (recipiente, i+1)
            worker = Thread(target=self._classificar, args=args)
            worker.start()
            threads.append(worker)

        vivas = self.nthreads
        for worker in threads:
            if worker.is_alive(): 
                worker.join()
        threads.clear()
        
        self._data_set = [[],[]]
        for recipiente in frame_set:
            self._data_set[0].extend(recipiente[0])
            self._data_set[1].extend(recipiente[1])
        
        print("[{}] Todas as Threads Finalizadas! Iniciando Treinamento.".format(sttwrn))
    
    def _classificar(self, recipiente, numero):
        frameAnterior = (None, -1)
        vis = visao.MegaMan(self.sprites)
        porcentagem = 0
        parte_100 = int(self._frames_thread * 0.1)
        
        print("[{}] Thread {} iniciada.".format(sttinf, numero))

        while len(recipiente[0]) < self._frames_thread:
            self._lock_video.acquire()
            frame = self._video.read()[1]
            self._lock_video.release()
            
            if frame is None:
                return

            frame = cv2.resize(frame, (256, 240))[:-16,:]
            
            # atualizar o estado do objeto megaman usando o frame
            vis.atualizar(vis.transformar(frame), 20)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            for s in (0.5, 0.5, 0.75):
                frame = cv2.resize(frame, None, fx=s, fy=s, interpolation=cv2.INTER_BITS)
            frame[frame <= 40] = 0

            # treina a rede com o frame anterior e o rótulo do frame atual
            # apenas nas transições
            temAnterior = not frameAnterior[0] is None
            
            if temAnterior:
                # coloca no dataset
                recipiente[0].append(frameAnterior[0].flatten())
                recipiente[1].append(vis.rotulo)
                
            # atualiza o frame anterior
            frameAnterior = (frame, vis.rotulo)

            if self.nthreads > 1:
                if len(recipiente[0]) % parte_100 == 0:
                    print("[{}] Thread {} {}%".format(sttinf, numero, porcentagem * 10))
                    porcentagem += 1
            else:
                self._exibirInfoTreinamento(self.frames, len(recipiente[0]))
        
        print("[{}] Fim classificação Thread {}.".format(sttinf, numero))
        
    def _treinar(self):
        """Executa o treinamento em um video"""
        self.framesTotal = int(self._video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.feitos = 0

        # Lê o video até o fim
        while True:
            
            if not ((self.framesTotal - self.feitos) >= self.frames):
                print("[{}] Não tem frames suficientes para completar o batch!".format(sttinf))
                break
            
            self._iniciarClassificacao()

            if len(self._data_set[0]) > 0:
                if self._rnn:
                    self._fitRNN()
                else:
                    self._fit()
                self.feitos += len(self._data_set[0])
                
                print("[{}] Fim do treinamento do batch. {}% Completo".format(sttwrn, int((self.feitos/self.frames)*100)))

                # limpa o batch
                self._data_set[0].clear()
                self._data_set[1].clear()
        
    def _atualizarLog(self, historico):
        info = Info(
            acc = list(map(float, historico.history['accuracy'])), 
            loss = list(map(float, historico.history['loss'])),
            rotulos = self._data_set[1],
            tam_batch = len(self._data_set[0]))
        
        self._log.write(str(info))
        
    def _fit(self):
        treinar = True
        epochs = self.epochs
        ultimo = 0

        while treinar:
            historico = inteligencia.modelo.fit(
                numpy.array(self._data_set[0])/255.0, 
                numpy.array(self._data_set[1]),
                batch_size=self.batch_size,
                epochs=epochs, 
                verbose=1, 
                shuffle=self.suffle)

            self._atualizarLog(historico)
            
            atual = numpy.mean(historico.history["acc"])
            treinar = ((atual <= 0.80) or ((atual - ultimo) > 0.005))
            print("\033[31mVariação: ", (atual - ultimo), "\033[0;0m")
            ultimo = atual
    
    def _fitRNN(self):
        treinar = True
        while treinar:
            gerador = TimeseriesGenerator(
                numpy.array(self._data_set[0])/255.0, 
                numpy.array(self._data_set[1]), 
                length=self.time_steps,
                batch_size=self.batch_size)
            historico = inteligencia.modelo.fit_generator(
                gerador,
                epochs=self.epochs,
                shuffle=self.suffle,
                verbose=1)
            self._atualizarLog(historico)

            if self._iterativo:
                try:
                    treinar = input("Continuar (s/n)? ") == 's'
                except:
                    treinar = False
            else:
                treinar = False
        
    def _exibirInfoTreinamento(self, total, feitos):
        """Print de informações sobre o andamento do treinamento"""
        progresso = int((feitos/total)*100)
        texto = "\rProgresso: [{}] {}% {}"
        statBatch = "{}/{}".format(feitos, total)
        preenchimento = "="*int(progresso/4)+"\033[1;94m>\033[0;0m"+"."*(int(100/4)-int(progresso/4))
        print(texto.format(preenchimento, progresso, statBatch), end="")
        if progresso == 100: print("")
        
class Info:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
    
    def __str__(self):
        return yaml.dump({datetime.now().isoformat(): self.__dict__})
