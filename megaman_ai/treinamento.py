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
import timeit
from datetime import datetime

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
        self._frameAnterior = None, -1
        self._s = [],[]
        self._rodada = 0
        self._log = open("logs/"+self.nome+".log", "a")

    def iniciar(self):
        """Inicia o treinamento em todos os videos"""

        for video in self.videos:

            # Abre o video
            videoCapture = cv2.VideoCapture(video)

            # Exibe algumas informações antes do inicio do treinamento
            self._exibirInfosInicioTreinamento(video)

            try:
                # Chama a função de treinamento para o video atual
                self._treinar(videoCapture)

            # Trata o caso de iterrupção pelo usuário via teclado
            # Para salvar o progresso do video
            except KeyboardInterrupt:
                print("Iterrompido pelo usuário.")

            # Exibe informações no fim do treinamento
            self._exibirInfosFimVideo(video)
            
            # Salva modelo
            inteligencia.salvar()

    def _exibirInfosFimVideo(self, video):
        """Exibe algumas informações antes do treinamento com o video"""
        inteligencia.modelo.summary()
        print("Fim de treinamento com o video {}".format(video))

    def _exibirInfosInicioTreinamento(self, video):
        """Exibe algumas informações depois do treinamento com o video"""
        self._log.write("{} - Iniciando treinamento: batch_size={} epochs={} videos={}".format(
            self.nome, self.epochs, self.batch_size, self.videos))

    def _treinar(self, videoCapture):
        """Executa o treinamento em um video"""
        
        self._s = [],[]
        self._rodada = 0
        
        # Lê o video até o fim
        while videoCapture.isOpened():
            # Obtém o frame do video e aplica tranformações iniciais
            frameBruto = videoCapture.read()[1]
            fimVideo = frameBruto is None

            if not fimVideo:
                frameRedimencionado = cv2.resize(frameBruto, (256, 240))
                frameTratado = visao.MegaMan.transformar(frameRedimencionado)
                
                # atualizar o estado do objeto megaman usando o frame
                self.visao.atualizar(frameTratado, 20)
                
                # treina a rede com o frame anterior e o rótulo do frame atual
                # apenas nas transições
                temAnterior = not self._frameAnterior[0] is None
                isTransicao = self._frameAnterior[1] != self.visao.rotulo
                temEstadoAtual = self.visao.rotulo != -1

                if temAnterior and isTransicao and temEstadoAtual:
                    # coloca no dataset
                    self._s[0].append(self._frameAnterior[0])
                    self._s[1].append(self.visao.rotulo)
                
            # atualiza o frame anterior
            self._frameAnterior = frameTratado,self.visao.rotulo

            # Verifica se está pronto para treinar
            prontoTreinar = len(self._s[0]) == self.batch_size 

            if  prontoTreinar or fimVideo:
                self._fit()
                # limpa o batch
                self._s[0].clear()
                self._s[1].clear()
                self._rodada += 1

            # Exibe informações do treinamento no console
            self._exibirInfoTreinamento(videoCapture)

            # Exibe a visão atual com alguns dados
            self._exibirVisaoTreinamento(frameTratado)

            # Quando a tecla 'q' é pressionada interrompe o treinamento
            if (cv2.waitKey(1) & 0xFF) == ord('q') or fimVideo:
                break

    def _atualizarLog(self, historico):
        historico = historico.history
        log_fmt = "{} - {} - rodada={} batch={}\nrotulos={}\n{}\n"
        formato = "epoch={:6.4} loss={:12.10} acc={:6.4}"
        data = datetime.now().isoformat()

        dados = "\n".join([formato.format(str(i), str(historico['loss'][i]), str(historico['acc'][i])) for i in range(self.epochs)])

        # envia os dados para o arquivo
        self._log.write(log_fmt.format(data, self.nome, self._rodada, len(self._s[0]), self._s[1], dados))

    def _fit(self):
        historico = inteligencia.modelo.fit(
            numpy.array(self._s[0])/255.0, 
            numpy.array(self._s[1]),
            batch_size=self.batch_size,
            epochs=self.epochs, 
            verbose=1, 
            shuffle=True)
        
        self._atualizarLog(historico)

    def _exibirInfoTreinamento(self, videoCapture):
        """Print de informações sobre o andamento do treinamento"""
        # Progresso
        frameAtual = int(videoCapture.get(cv2.CAP_PROP_POS_FRAMES))
        framesTotal = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
        progresso = int((frameAtual/framesTotal)*100)
        texto = "Progresso: [{}] {}% {}\r"
        statBatch = "{}/{}".format(len(self._s[0]), self.batch_size)
        preenchimento = "#"*int(progresso/4)+">"+"."*(int(100/4)-int(progresso/4))
        # imprime
        print(texto.format(preenchimento, progresso, statBatch), end="")

    def _exibirVisaoTreinamento(self, frame):
        """Mostra a visão do treinamento"""
        if self.exibir:
            #* Comentado pois se tornou desnecessário
            # progresso = self.estatisticas.progresso
            # qualidade = self.estatisticas.qualidadeAtual
            # self.visao.desenhar_infos(frame, progresso, qualidade)
            cv2.imshow("Treinamento", frame)
