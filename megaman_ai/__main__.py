import megaman_ai
import getopt
import sys  
import os
import yaml

opcoes = "hCTtcmes:i:"

class Params:
    jogar           = True
    coleta          = False
    exibir_visao    = False
    arquivo_config  = ["~/.megaman_ai.yaml", "megaman.yaml"]
    carregar_estado = False
    focar           = False
    sequencia       = [1]
    frames_seg      = 60
    estats_temp     = False
    ajuda           = False
    skip_to         = 0

    def __init__(self, params, sobra):
        for param in params:
            if "-h" in param[0]:
                self.ajuda = True
            if "-C" in param[0]:
                self.jogar  = False
                self.coleta = True
            if "-e" in param[0]:
                self.exibir_visao = True
            if "-a" in param[0]:
                self.arquivo_config.insert(0, param[1])
            if "-m" in param[0]:
                self.focar = True
            if "-c" in param[0]:
                self.carregar_estado = True
            if "-s" in param[0]:
                self.sequencia = param[1].split(",")
            if "-f" in param[0]:
                self.frames_seg = int(param[1])
            if "-T" in param[0]:
                self.estats_temp = True
            if "-i" in param[0]:
                self.skip_to = int(param[1])
        self.sobra = sobra

def uso():
    print("Megaman AI")
    print("")
    print("Desafio de Inteligencia Artificial para jogar o jogo Megaman 3.")
    print("")
    print("Uso:")
    print("  jogar  : python3 -m megaman_ai")
    print("  treinar: python3 -m -megaman_ai -C")
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
    print("  -T:    Exibe estatísticas sobre o tempo dos frames.")
    print("  -i:    (0...) Skipa o video até um determinado frame.")
    print("")
    exit(3)

def main(params):
    if params.ajuda:
        uso()
    elif params.coleta:
        megaman_ai.coleta.iniciar(
                skip_to    = params.skip_to,
                exibir     = params.exibir_visao,
                estats_temp= params.estats_temp)
    elif params.jogar:
        megaman_ai.jogar(
                room      = "arquivos/MegaMan3.nes",
                sequencia = params.sequencia, 
                focar     = params.focar,
                carregar  = params.carregar_estado)

if __name__ == "__main__":
    try:
        params,sobra = getopt.getopt(sys.argv[1:], opcoes)
        params       = Params(params, sobra)
    except:
        print("Argumentos inválidos!")
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

    try:
        main(params)
    except KeyboardInterrupt:
        print("Execução interrompida pelo usuário")
        exit(0)