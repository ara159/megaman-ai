from os import environ, kill, getpid
import signal

from . import parametros, inteligencia, treinamento, jogo
from tensorflow.python.util import deprecation

# disable warning messages
deprecation._PRINT_DEPRECATION_WARNINGS = False
environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def uso():
    print("Megaman AI")
    print("")
    print("Trabalho de TCC - Rafael Costa e Robson Santos")
    print("")
    print("O objetivo do projeto é criar uma inteligência artificial")
    print("  capaz de jogar pelo menos uma fase de MegaMan3.")
    print("")
    print("O programa se divide em duas partes: Treinamento e Jogo.")
    print("No Treinamento é onde será lido os videos para treinar a rede e")
    print("  no modo Jogo é onde o conhecimento da rede será usado para jogar.")
    print("")
    print("Uso:")
    print("  Para entrar no modo JOGAR:")
    print("     python3 -m megaman_ai [opções]")
    print("")
    print("  Para entrar no modo TREINAMENTO:")
    print("     python3 -m megaman_ai --treinamento <videos> [opções]")
    print("")
    print("Opções Gerais:")
    print("  --ajuda:")
    print("       Exibe esta mensagem de ajuda.")
    print("  --config=<caminho>")
    print("       Caminho para um arquivo de configuração yaml.")
    print("  --time_steps=<int>")
    print("       Salto de tempo em frames.")
    print("  --nome=<nome inteligencia>:")
    print("       Caso a inteligencia exista ela é carregada.")
    print("       Caso não exista, será necessário cria-la, olhe o arquivo nova.py.")
    print("  --sprites=<caminho>:")
    print("       Arquivo yaml com as informações de sprites.")
    print("  --fps=<int>:")
    print("       Numero de fps usados para treinamento e jogo. Os valores aceitos")
    print("       são 30, 15, 10 ou 5.")
    print("")
    print("Opções modo Treinamento:")
    print("  --epochs=<int>:")
    print("       Número de épocas para cada batch. Padrão: 50.")
    print("  --batch_size=<int>:")
    print("       Tamanho do batch de treinamento.")
    print("  --nthreads=<int>:")
    print("       Quantidade de threads para a classificação do video.")
    print("       Por padrão é 4.")
    print("  --suffle:")
    print("       Se deve misturar as imagens que são passadas para o treinamento.")
    print("       Por padrão é verdadeiro.")
    print("  --frames:")
    print("       Quantidade de frames a serem processados e passados e usados como")
    print("       dataset do treinamento.")
    print("")
    print("Opções modo Jogar:")
    print("  --room=<arquivo room>:")
    print("       Arquivo de room do jogo. Padrão: ./MegaMan3.nes")
    print("  --carregar-pre:")
    print("       Carrega um estado pré carregado do emulador. Padrão: False")
    print("  --fceux=<caminho>:")
    print("       Caminho para o executavél do emulador fceux. Padrão: /usr/games/fceux")
    print("  --fceux_script=<caminho>:")
    print("       Caminho para o script lua 'servidor'. Padrão: ./server.lua")
    print("")
    exit(3)


def treinar(params):
    """Verifica os parâmetros para treinamento e
    inicia com as opções recebidas"""
    
    if not params.validarTreinamento():
        exit(3)
    
    # carrega a inteligência
    inteligencia.carregar(params.nome)
    
    treino = treinamento.Treinamento(
        videos=params.videos,
        sprites=params.sprites,
        epochs=params.epochs,
        batch_size=params.batch_size,
        nome=params.nome,
        nthreads=params.nthreads,
        time_steps=params.time_steps,
        suffle=params.suffle,
        frames=params.frames,
        fps=params.fps)
    
    treino.iniciar()

def jogar(params):
    """Verifica os parâmetros para jogar e
    inicia com as opções recebidas"""

    if not params.validarJogar():
        exit(3)
    
    # carrega a inteligência
    inteligencia.carregar(params.nome)

    jogar = jogo.Jogo(
        room = params.room,
        sprites = params.sprites,
        fceux=params.fceux,
        time_steps=params.time_steps,
        fceux_script=params.fceux_script,
        fps=params.fps)
    
    jogar.iniciar()

if __name__ == "__main__":
    # Recebe parâmetros via linha de comando
    try:
        params = parametros.parse()
    except Exception as erro:
        print(erro)
        uso() # exit

    # Exibe informações de ajuda se for necessário
    if params.ajuda: 
        uso() # exit
    
    # Modo treinameto
    if params.treinamento:
        treinar(params)
    
    # Modo jogar
    else:
        jogar(params)

    kill(getpid(), signal.SIGKILL)