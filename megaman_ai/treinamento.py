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
import megaman_ai
import timeit

from megaman_ai import inteligencia

class Treinamento:
    """Armazena informações sobre uma instancia de treinamento
    incluindo estatísticas sobre o andamento do treinamento."""

    def __init__(self, videos, sprites, historico=None, destino="", 
            exibir=False, tempo=False, qualidade=False):
        self.videos = videos
        self.destino = destino
        self.tempo = tempo
        self.exibir = exibir
        self.qualidade = qualidade
        self.visao = megaman_ai.visao.MegaMan(sprites)
        self.dimensaoTela = (256, 240)
        self.estatisticas = Estatisticas()
        self.frameAnterior = None, -1
        self.usarHistorico = not historico is None
        self.arquivoHistorico = historico
        self.historico = None
        self.epochs = 50
        self.batch_size = 100
        self.s = [],[]
        self._obterHistorico()

    def iniciar(self):
        """Inicia o treinamento em todos os videos"""

        for video in self.videos:
            
            # Abre o video
            videoCapture = cv2.VideoCapture(video)

            # Verifica se o video já foi iniciado anteriormente
            self._continuar(video, videoCapture)

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
            self._exibirInfosFimTreinamento(video)

            # Após o treinamento com o video, atualiza o histórico
            self._atualizarHistorico(video, videoCapture)
            
            # Salva modelo
            inteligencia.salvar()

    def _exibirInfosFimTreinamento(self, video):
        """Exibe algumas informações antes do treinamento com o video"""
        inteligencia.modelo.summary()
        print("Fim de treinamento com o video {}.".format(video))

    def _exibirInfosInicioTreinamento(self, video):
        """Exibe algumas informações depois do treinamento com o video"""
        print("Iniciando treinamento video {}.".format(video))

    def _continuar(self, video, videoCapture):
        """Tenta continuar o treinamento do video"""
        # Verifica se é para usar o histórico
        if not self.usarHistorico:
            return

        # Caso possa

        # Se o histórico for None (primeira execução)
        elif self.historico is None:

            # Inicia uma estatística zerada
            self.estatisticas.iniciar()

        # Se não for None e video é chave
        elif video in self.historico:
            
            # Atualiza as estatisticas do treinamento para as que estavam anteriormente
            self.estatisticas = self.historico[video]
            
            # Skipa o video para o último frame do historico
            if videoCapture.set(cv2.CAP_PROP_POS_FRAMES, self.estatisticas.frameAtual):
                return
            
            # Se não conseguir skipar, recomeça do inicio do video
            else:
                print("Não foi possivel continuar o treinamento com o video {}".format(video))

        # Se não conseguir skipar, ou o video não estiver no histórico, inicia do zero o video
        self.estatisticas.iniciar()
        
        return

    def _obterHistorico(self):
        """Obtém o histórico e retorna"""
        # Verifica se é para usar o histórico
        if not self.usarHistorico:
            return None
        
        # Abre o arquivo e lê como yaml
        arquivo = open(self.arquivoHistorico, 'r')
        self.historico = yaml.load(arquivo.read())
        arquivo.close()

    def _atualizarHistorico(self, videoNome, videoCapture):
        """Atualiza o arquivo de histórico com os dados mais recentes do video"""
        #! disabilitado para debugar
        # Verifica se é para usar o histórico
        # if not self.usarHistorico:
        #     return
        
        # # Se o historico atual for None (normalmente a primeira execução)
        # if self.historico is None:

        #     # Inicializa um dict
        #     self.historico = {}
        
        # # Seta a chave como sendo o caminho do video e o valor sendo as estatisticas
        # self.historico[videoNome] = self.estatisticas

        # # Atualiza as informações
        # arquivo = open(self.arquivoHistorico, 'w')
        # arquivo.write(yaml.dump(self.historico))

    def _treinar(self, videoCapture):
        """Executa o treinamento em um video"""
        
        self.s = [],[]

        # Lê o video até o fim
        while videoCapture.isOpened():
            # Obtém o frame do video e aplica tranformações iniciais
            frameBruto = videoCapture.read()[1]
            fimVideo = frameBruto is None

            if not fimVideo:
                frameRedimencionado = cv2.resize(frameBruto, self.dimensaoTela)
                frameTratado = megaman_ai.visao.MegaMan.transformar(frameRedimencionado)
                
                # atualizar o estado do objeto megaman usando o frame
                qualidade = self.visao.atualizar(frameTratado, 20)
                
                # treina a rede com o frame anterior e o rótulo do frame atual
                # apenas nas transições
                if not self.frameAnterior[0] is None and \
                    self.frameAnterior[1] != self.visao.rotulo and \
                    self.visao.rotulo != -1:
                    self.s[0].append(self.frameAnterior[0])
                    self.s[1].append(self.visao.rotulo)
                
                # atualiza o frame anterior
                self.frameAnterior = frameTratado,self.visao.rotulo
                
            if len(self.s[0]) == self.batch_size or fimVideo: # ou fim do video
                inteligencia.modelo.fit(
                    numpy.array(self.s[0])/255.0, 
                    numpy.array(self.s[1]),
                    batch_size=self.batch_size,
                    epochs=self.epochs)
                # limpa o batch
                self.s[0].clear()
                self.s[1].clear()

            # Atualiza as estatísticas com os novos dados
            # TODO: A qualidade deve ser atualizada a cada frame que pega, 
            # neste momento está sendo calculado errado
            # talvez retirar essa estatística seja uma opção
            self.estatisticas.atualizar(videoCapture, 0) 

            # Exibe informações do treinamento no console
            self._exibirInfoTreinamento()

            # Exibe a visão atual com alguns dados
            self._exibirVisaoTreinamento(frameTratado)

            # Quando a tecla 'q' é pressionada interrompe o treinamento
            if (cv2.waitKey(1) & 0xFF) == ord('q') or fimVideo:
                break

    def _exibirInfoTreinamento(self):
        """Print de informações sobre o andamento do treinamento"""

        # Progresso
        progresso = self.estatisticas.progresso
        print("Progresso: [{}] {}% {}\r".format(
                "#"*int(progresso/4)+">"+"."*(int(100/4)-int(progresso/4)),
                progresso,
                "{}/{}".format(len(self.s[0]), self.batch_size)),
            end="")

    def _exibirVisaoTreinamento(self, frame):
        """Mostra a visão do treinamento"""

        if self.exibir:
            progresso = self.estatisticas.progresso
            qualidade = self.estatisticas.qualidadeAtual
            self.visao.desenhar_infos(frame, progresso, qualidade)


class Estatisticas:
    """Armazena as informações sobre o desempenho do treinamento"""
    framesTotal = None
    frameAtual = 0
    progresso = 0
    qualidadeAtual = 0
    qualidadeTotal = 0
    qualidadeMedia = 0
    tempoTotal = 0
    tempoMedioFrame = 0
    tempoInicial = 0

    def iniciar(self):
        """Inicia as estatísticas"""

        # Seta o tempoInicial
        self.tempoInicial = timeit.default_timer()

    def atualizar(self, videoCapture, qualidadeAtual):
        """Recebe e atualiza as informações"""

        # Atualiza os contadores
        self.framesTotal = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frameAtual = int(videoCapture.get(cv2.CAP_PROP_POS_FRAMES))
        self.progresso = int((self.frameAtual / self.framesTotal) * 100)
        self.qualidadeTotal += qualidadeAtual
        self.qualidadeMedia = self.qualidadeTotal / self.frameAtual
        diferenca = timeit.default_timer() - self.tempoInicial
        self.tempoTotal += diferenca
        self.tempoMedioFrame = self.tempoTotal / self.frameAtual
        self.tempoInicial = timeit.default_timer()
