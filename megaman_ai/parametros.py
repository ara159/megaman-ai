"""
parametros.py

Funções para tratamento dos parâmetros recebidos via
linha de comando.
"""

from sys import argv
from os import path, mkdir, getuid
from getopt import gnu_getopt
import yaml
import socket

class Parametros:
    """ Armazena as opções recebidas pelo usuário via linha 
    de comando para a execução do programa.
    Os atributos já iniciam com os valores padrão.
    A lista de parâmetros é criada a partir dos atributos da classe.
    """
    treinamento = False
    exibir = False
    sprites = "megaman.yaml"
    ajuda = False
    qualidade = False
    tempo = False
    not_suffle = False
    room = "MegaMan3.nes"
    fceux = "/usr/games/fceux"
    fceux_script = "server.lua"
    nome = ""
    epochs = 50
    batch_size = 300
    nthreads = 4
    config = ""
    time_steps = 10

    def __init__(self, opts):
        self.parse(opts)

    def parse(self, opts):
        """Preenche o objeto com as opções recebidas"""
        # Configura os parâmetros que são esperados
        for parametro, valor in opts[0]:
            if "--" in parametro and len(valor) == 0:
                setattr(self, parametro[2:], True)
            else:
                setattr(self, parametro[2:], valor)
        
        # Configura os valores extras de parâmetro
        self.videos = opts[1]

        # converte valores
        self.epochs = int(self.epochs)
        self.batch_size = int(self.batch_size)
        self.nthreads = int(self.nthreads)
        self.time_steps = int(self.time_steps)

    @staticmethod
    def getopts():
        """Recupera a lista de objetos que podem ser recebidos
        por parâmetro do usuário, a lista é gerada baseada nos
        atributos da classe"""
        opts = []
        for attr in Parametros.__dict__.keys():
            if "__" in attr:
                continue
            
            tipoattr = type(getattr(Parametros, attr))
            
            if tipoattr.__name__ == "function":
                continue
            
            if tipoattr.__name__ == "bool":
                opts.append(attr)
            else:
                opts.append(attr+"=")

        return opts

    def _validarGeral(self):
        tudoOk = True
        # TODO: Mudar a verificação de sprites para cá
        if len(self.nome) == 0:
            print("É necessário passar o nome da inteligencia.")
            tudoOk = False
        if not path.isfile("modelos/"+self.nome+".h5"):
            print("A inteligência {} não existe em modelos.".format(self.nome))
            tudoOk = False
        return tudoOk

    def validarTreinamento(self):
        """Executa a validação das informações recebidas
        para o modo treinamento"""
        
        # TODO: Verificar se os videos passados são do formato aceito

        tudoOk = self._validarGeral()

        # Verifica existência do arquivo de sprites
        if not path.isfile(self.sprites):
            print("Arquivo sprites {} não existe.".format(self.sprites))
            tudoOk = False

        # Abre o arquivo sprites como yaml
        try:
            self.sprites = yaml.load(open(self.sprites).read())
        except:
            print("Não foi possível abrir o arquivo {} como yaml.".format(self.sprites), end="")
            print("Verifique se a sintaxe está correta.")
            tudoOk = False
        
        # verifica se os caminhos dos sprites estão corretos
        pastaSprites = self.sprites["sprites"]
        pastaMascaras = self.sprites["mascaras"]
        extencao = self.sprites["extencao"]

        for pasta in [pastaSprites, pastaMascaras]:
            if path.isdir(pasta):
                for estado in self.sprites["estados"]:
                    for sprite in self.sprites["estados"][estado]['sprites']:
                        arquivo = pasta+"/"+sprite+"."+extencao
                        if not path.isfile(arquivo):
                            print("O arquivo '{}' de sprite não existe.".format(arquivo))
                            tudoOk = False
            else:
                print("Pasta '{}' não existe.".format(pasta))
                tudoOk = False

        # Verifica se os videos foram passados
        if len(self.videos) == 0:
            print("Nenhum video passado para o treinamento.")
            print("É necessário passar pelo menos 1 video.")
            tudoOk = False

        # Verifica se os videos passados existem
        for video in self.videos:
            if not path.isfile(video):
                print("Video {} não encontrado.".format(video))
                tudoOk = False
        
        # Verifica a quantidade de Threads
        if self.nthreads < 0:
            print("Número de threads inválido.")
            tudoOk = False

        return tudoOk

    def validarJogar(self):
        """Executa a validação das informações recebidas
        para o modo jogar"""

        tudoOk = self._validarGeral()
        
        # TODO: Verificar se o fceux está instalado

        # Testa se está executando com permissões
        if getuid() != 0:
            print("É necessário executar como administrador.")
            tudoOk = False
        
        # testa se a porta 4321 está disponível
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("127.0.0.1", 4321))
            sock.close()
        except OSError:
            print("Porta 4321 está ocupada.")
            tudoOk = False

        # Verifica se existe a room recebida
        if not path.isfile(self.room):
            print("Não foi encontrado o arquivo {} do parâmetros room.".format(self.room))
            tudoOk = False
        
        # Verifica se existe a room recebida
        if not path.isfile(self.fceux):
            print("Não foi encontrado o executavél do fceux.".format(self.room))
            tudoOk = False

        # Verifica se existe o arquivo script do fceux
        if not path.isfile(self.fceux_script):
            print("Não foi o arquivo de script do fceux (servidor).".format(self.room))
            tudoOk = False
        
        return tudoOk

def parse():
    """Cria, preenche e retorna um objeto `Parametro`"""
    # TODO: Verificar a necessidade de se ter parâmetros curtos
    opts_curta = ""
    opts_longa = Parametros.getopts()
    args = argv[1:]
    opts = gnu_getopt(args, opts_curta, opts_longa)
    parametros = Parametros(opts)
    if len(parametros.config) > 0 and path.exists(parametros.config):
        parametros.__dict__ = yaml.load(open(parametros.config, "r").read())
    return parametros