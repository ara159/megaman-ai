import getopt
import megaman_ai
import sys  
import os
import yaml

opcoes = "Chqtcmed:s:i:"

class Params:
    # Parametros gerais
    arquivo_config  = ["~/.megaman_ai.yaml", "megaman.yaml"]
    ajuda           = False
    # Parametros para jogar
    jogar           = True
    carregar_estado = False
    focar           = False
    sequencia       = [1]
    # Parametros de treinamento
    frame_inicial   = 0
    coleta          = False
    exib_tempo      = False
    exib_video      = False
    exib_qualidade  = False
    pasta_dst       = ""

    def __init__(self, params, sobra):
        for param in params:
            # Parametros gerais
            if "-h" in param[0]:
                self.ajuda = True
            if "-a" in param[0]:
                self.arquivo_config.insert(0, param[1])
            # Parametros jogar
            if "-m" in param[0]:
                self.focar = True
            if "-c" in param[0]:
                self.carregar_estado = True
            if "-s" in param[0]:
                self.sequencia = param[1].split(",")
            # Parametros de coleta
            if "-C" in param[0]:
                self.jogar  = False
                self.coleta = True
            if "-e" in param[0]:
                self.exib_video = True
            if "-t" in param[0]:
                self.exib_tempo = True
            if "-i" in param[0]:
                self.frame_inicial = int(param[1])
            if "-q" in param[0]:
                self.exib_qualidade = True
            if "-d" in param[0]:
                self.pasta_dst = param[1]
        self.sobra = sobra

def uso():
    print("Megaman AI")
    print("")
    print("Desafio de Inteligencia Artificial para jogar o jogo Megaman 3.")
    print("")
    print("Uso:")
    print("  jogar  : python3 -m megaman_ai")
    print("  treinar: python3 -m -megaman_ai -C <video 1> [<video 2> ...]")
    print("")
    print("Parâmetros gerais:")
    print("  -a:    Arquivo de configuração.")
    print("  -h:    Exibe esta mensagem de ajuda.")
    print("")
    print("Parâmetros modo jogar:")
    print("  -c:    Carrega um estado pré carregado no emulador.")
    print("  -m:    Mantém a tela do game focada durante o jogo.")
    print("  -s:    (1,2,3,...8) Sequência de fases a ser seguida.")
    print("         Numeros separados por vírgula. Caso seja omitido, será")
    print("         sequencial de 1 a 8.")
    print("")
    print("Parâmetros modo coleta:")
    print("  -e:    Exibir saida da visão.")
    print("  -q:    Exibe informações sobre a qualidade de cada frame coletado")
    print("  -t:    Exibe estatísticas sobre o tempo dos frames.")
    print("  -i:    (0...) Skipa o video até um determinado frame.")
    print("  -d:    Pasta de destino. Caso seja omitido, será a pasta atual.")
    print("")
    exit(3)

def main(params):
    if params.ajuda: 
        uso()
    
    if params.coleta:
        megaman_ai.coleta.iniciar(
                videos = params.sobra,
                pasta_dest = params.pasta_dst,
                frame_inicial = params.frame_inicial,
                exib_video = params.exib_video,
                exib_tempo = params.exib_tempo,
                exib_qualidade = params.exib_qualidade)
    elif params.jogar:
        megaman_ai.jogar(
                room = "MegaMan3.nes",
                sequencia = params.sequencia, 
                focar = params.focar,
                carregar = params.carregar_estado,
                foco_tx = 0.3,   # TODO: Parametrizar
                escala = 2,     # TODO: Parametrizar
                exibir = False) # TODO: Parametrizar

def parseParametros():
    try:
        params,sobra = getopt.getopt(sys.argv[1:], opcoes)
        params       = Params(params, sobra)
    except Exception as erro:
        print("Argumentos inválidos!", erro)
        uso()

    arquivo = None

    for arquivo in params.arquivo_config:
        if os.path.isfile(arquivo):
            arquivo = open(arquivo, "r").read()
            break
    else:
        print("Não foi possível encontrar um arquivo de configuração.")
        exit(2)

    try:
        megaman_ai.config.__dict__ = yaml.load(arquivo)
    except:
        print("Houve problemas com a leitura do aquivo de configuração.")
        print("Verifique a sintaxe yaml do arquivo.")
        exit(2)
    
    return params

def executar(params):
    try:
        main(params)
    except KeyboardInterrupt:
        print("Execução interrompida pelo usuário")
        exit(0)

if __name__ == "__main__":
    params = parseParametros()
    executar(params)
