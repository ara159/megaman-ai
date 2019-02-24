import megaman_ai
import getopt
import sys  
import os
import yaml

opcoes = "hCTtcmves:f:"

class Config: pass

class Params:
    jogar           = True
    coleta          = False
    verboso         = False
    exibir_visao    = False
    arquivo_config  = ["~/.megaman_ai.yaml", "megaman.yaml"]
    carregar_estado = False
    focar           = False
    sequencia       = [1]
    frames_seg      = 30
    estats_temp     = False
    ajuda           = False

    def __init__(self, params, sobra):
        for param in params:
            if "-h" in param[0]:
                self.ajuda = True
            if "-C" in param[0]:
                self.jogar  = False
                self.coleta = True
            if "-v" in param[0]:
                self.verboso = True
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
    print("  -v:    Modo verboso. Exibe informações sobre a execução.")
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
    print("  -f:    (1 a 60) Numero de frames por sergundo a serem processados.")
    print("         Caso omitido, o valor é de 30.")
    print("")
    exit(3)

def main(params, config):
    if params.ajuda:
        uso()
    elif params.coleta:
        megaman_ai.coleta.iniciar(
                config     = config, 
                frames_seg = params.frames_seg,
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
        config = Config()
        config.__dict__ = yaml.load(arquivo)
    except:
        print("Houve problemas com a leitura do aquivo de configuração.")
        print("Verifique a sintaxe yaml do arquivo.")
        exit(2)

    try:
        main(params, config)
    except KeyboardInterrupt:
        print("Execução interrompida pelo usuário")
        exit(0)