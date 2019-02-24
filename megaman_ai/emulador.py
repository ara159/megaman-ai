from threading import Thread
from time import sleep
import subprocess, shlex
from pynput.keyboard import Key, Controller


class Emulador(Thread):
	def __init__(self, room, posicao=(0,0), escala=2):
		super(Emulador, self).__init__()
		self.room    = room
		self.name    = room.split(".")[0].split("/")[-1]
		self.escala  = escala
		self.posicao = posicao
		self.comando = shlex.split("nestopia -d -s %d %s" % (self.escala,self.room))

	def run(self):
		retorno = subprocess.run(self.comando, 
								 stdout=subprocess.DEVNULL,
								 stderr=subprocess.DEVNULL)
		if retorno.returncode != 0:
			print("Não foi possivel iniciar o emulador")
		else:
			print("Fim Thread emulador")

class ManterEmulador(Thread):
	def __init__(self, emulador, taxa=0.5):
		super(ManterEmulador, self).__init__()
		self.emulador = emulador
		self.taxa     = taxa
		self.foco     = shlex.split("wmctrl -a \"%s\"" % self.emulador.name)
		args_posicao  = (emulador.name, emulador.posicao[0], emulador.posicao[1])
		self.posicao  = shlex.split("wmctrl -r \"%s\" -e 0,%d,%d,-1,-1" % args_posicao)

	def run(self):
		sleep(0.2)
		while self.emulador.isAlive():
			subprocess.run(self.foco, stderr=subprocess.DEVNULL)
			subprocess.run(self.posicao, stderr=subprocess.DEVNULL)
			if self.taxa < 0:
				break
			sleep(self.taxa)
		print("Fim Thread foco")

class Controle(Controller):
	pulo     = "z"
	disparo  = "a"
	esquerda = Key.left
	direita  = Key.right
	cima     = Key.up
	baixo    = Key.down
	pause    = Key.enter
	carregar = Key.f7

	pressionados = []

	def __init__(self, emulador):
		super(Controle, self).__init__()
		self.emulador = emulador

	def _click(self, botao):
		self.press(botao)
		sleep(0.05)
		self.release(botao)

	def pular(self, click=False, verify_emu=True):
		if not self.emulador.isAlive():
			return
		if click:
			self._click(self.pulo)
		else:
			self.press(self.pulo)
			self.pressionados.append(self.pulo)

	def disparar(self, click=False):
		if not self.emulador.isAlive():
			return
		if click:
			self._click(self.disparo)
		else:
			self.press(self.disparo)
			self.pressionados.append(self.disparo)

	def andar_direita(self, click=False):
		if not self.emulador.isAlive():
			return
		if click:
			self._click(self.direita)
		else:
			self.press(self.direita)
			self.pressionados.append(self.direita)

	def andar_esquerda(self, click=False):
		if not self.emulador.isAlive():
			return
		if click:
			self._click(self.esquerda)
		else:
			self.press(self.esquerda)
			self.pressionados.append(self.esquerda)

	def subir(self, click=False):
		if not self.emulador.isAlive():
			return
		if click:
			self._click(self.cima)
		else:
			self.press(self.cima)
			self.pressionados.append(self.cima)

	def descer(self, click=False):
		if not self.emulador.isAlive():
			return
		if click:
			self._click(self.baixo)
		else:
			self.press(self.baixo)
			self.pressionados.append(self.baixo)

	def pausar(self):
		if not self.emulador.isAlive():
			return
		self._click(self.pause)

	def soltar_pular(self):
		self.release(self.pulo)
		self.pressionados.remove(self.pulo)

	def soltar_disparar(self):
		self.release(self.disparo)
		self.pressionados.remove(self.disparo)

	def soltar_andar_direita(self):
		self.release(self.direita)
		self.pressionados.remove(self.direita)

	def soltar_andar_esquerda(self):
		self.release(self.esquerda)
		self.pressionados.remove(self.esquerda)

	def soltar_subir(self):
		self.release(self.cima)
		self.pressionados.remove(self.cima)

	def soltar_descer(self):
		self.release(self.baixo)
		self.pressionados.remove(self.baixo)

	def soltar_controle(self):
		for botao in self.pressionados:
			self.release(botao)
