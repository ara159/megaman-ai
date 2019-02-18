from threading import Thread
from time import sleep
import subprocess, shlex
from pynput.keyboard import Key, Controller

# DEBUG: A thred ManterEmulador ficará ativa após o fechamento da
#		thred Emulador no ``máximo`` o tempo do `delay`

class Emulador(Thread):
	def __init__(self, room, posicao_tela=(0,0), escala=2):
		super(Emulador, self).__init__()
		self.room = room
		self.name = room.split("/")[-1].split(".")[0]
		self.escala = escala
		self.posicao = posicao_tela

	def run(self):
		args = shlex.split("nestopia -s "+str(self.escala)+" "+self.room)
		retorno = subprocess.run(args, stdout=subprocess.DEVNULL,
									stderr=subprocess.DEVNULL) # Bloqueia a thread
		if retorno.returncode != 0:
			print("Não foi possivel iniciar o emulador")
		else:
			print("Emulador finalizado")

class ManterEmulador(Thread):
	def __init__(self, th_emulador, delay):
		super(ManterEmulador, self).__init__()
		self.emulador = th_emulador
		# foco
		self.cmd_foco = shlex.split("wmctrl -a '"+th_emulador.getName()+"'")
		# posicao
		pos = str(th_emulador.posicao[0])+","+str(th_emulador.posicao[1])
		self.cmd_posicao = shlex.split("wmctrl -r '"+th_emulador.getName()+"' -e 0,"+pos+",-1,-1")

		self.delay = delay

	def run(self):
		while self.emulador.isAlive():
			subprocess.run(self.cmd_foco)
			subprocess.run(self.cmd_posicao)
			sleep(self.delay)

class Controle(Controller):
	pulo = "z"
	disparo = "a"
	esquerda = Key.left
	direita = Key.right
	cima = Key.up
	baixo = Key.down
	pause = Key.enter
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
