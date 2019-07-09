from threading import Thread
import subprocess
import shlex
import time
import socket
import json
import os
import cv2

# TODO: Usar um "whereis" para encontrar o caminho do executável do emulador


class Jogo:

    def __init__(self, room, fceux="/usr/games/fceux", fceux_script="server.lua", sequencia=None, carregar_pre=False):
        self.room = room
        self.sequencia = sequencia
        self.carregar_pre = carregar_pre
        self.fceux = fceux
        self.fceux_script = os.path.abspath(fceux_script)
        self._emulador = Thread(target=self._iniciarEmulador)
        self._conexao = None
        self._conectado = False
        self._caminhoFrame = "/tmp/.megamanAI.screen"

    def iniciar(self):
        # inicia o emulador
        self._emulador.start()
        # conecta ao emulador
        self._conectar()

        # enquanto o emulador estiver ativo E conectado
        while self._emulador.isAlive() and self._conectado:
            # executa a função jogar
            self._jogar()

        # verifica se o emulador continua ativo (caso tenha dado algum erro com o servidor)
        if self._emulador.isAlive():
            # join no emulador
            self._emulador.join()

    def obterFrame(self):
        """Obtém o frame atual do emulador"""
        try:
            # Recebe uma mensagem de 'pode ler a tela'
            self._conexao.recv(4096)

            # Tenta ler a tela em 5 tentativas,
            # se não conseguir retorna None
            frame = None
            tentativas = 5

            while frame is None and tentativas:
                frame = cv2.imread(self._caminhoFrame)
                tentativas -= 1

            # TODO: Logging DEBUG
            return frame

        except ConnectionResetError:
            print("-- Conexão fechada pelo servidor.")
            self._conectado = False
            return

    def _jogar(self):
        # TODO: Implementar
        # Lógica de jogo aqui
        pass

    def _iniciarEmulador(self):
        """Inicia a thread do emulador com os parâmetros passados"""

        # define o comando
        comando = shlex.split("{fceux} --nogui {room} --xscale 2 --yscale 2 --loadlua {fceux_script}".format(
            fceux=self.fceux,
            room=self.room,
            fceux_script=self.fceux_script))

        # executa, essa chamada trava a thread até o fim da execução
        processo = subprocess.run(
            comando, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        # verifica o código de saída do comando
        if processo.returncode == 0:
            print("Emulador finalizado normalmente.")
        else:
            print("Houve algum erro na execução do emulador.")

    def _conectar(self):
        """Se conecta ao emulador"""
        try:
            # Espera um tempinho para dar tempo de começar a executar o servidor
            time.sleep(2)
            # tenta se conectar
            self._conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._conexao.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self._conexao.connect(("127.0.0.1", 4321))
            print("-- Conectado ao emulador")
            self._conectado = True
        except ConnectionRefusedError:
            print("-- Conexão recusada pelo emulador.")

    def _enviarComando(self, comando):
        """Envia um comando para o emulador em formato JSON, o comando deve estar 
        na forma de dicionário."""
        try:
            self._conexao.send((json.dumps(comando)+"\n").encode())
        except BrokenPipeError:
            print("-- Conexão fechada pelo servidor.")
            self._conectado = False
