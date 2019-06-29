from threading import Thread
from time import sleep
import subprocess, shlex

class Emulador(Thread):
	def __init__(self, room):
		super(Emulador, self).__init__()
		self.room    = room
		self.comando = shlex.split("/usr/games/fceux MegaMan3.nes --loadlua /home/rafael/megaman-ai/server/lua_rafael.lua --xscale 2 --yscale 2")

	def run(self):
		retorno = subprocess.run(self.comando)
		if retorno.returncode != 0:
			print("Não foi possivel iniciar o emulador")
		else:
			print("Fim Thread emulador")
