import megaman_ai

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
    print("")
    print("Opções modo Treinamento:")
    print("  --sprites=<caminho>:")
    print("       Arquivo yaml com as informações de sprites.")
    print("  --historico=<caminho>:")
    print("       Onde o arquivo de histórico será criado e consultado.")
    print("       Por padrão ficará em '~/.megaman_ai/historico.yaml'")
    print("  --exibir:")
    print("       Exibir saida da visão com estátisticas sobre o treinamento.")
    print("  --qualidade:")
    print("       Exibe informações sobre a qualidade de cada frame observado.")
    print("  --carregar_pre:")
    print("       Carrega um estado pré carregado no emulador.")
    print("  --tempo:")
    print("       Exibe estatísticas sobre o tempo dos frames.")
    print("  --skip=<frame_num>:")
    print("       Skipa o video até um determinado frame.")
    print("  --destino=<caminho>:")
    print("       Pasta de destino. Caso seja omitido, será a pasta atual.")
    print("")
    print("Opções modo Jogar:")
    print("  --room=<arquivo room>:")
    print("       Arquivo de room do jogo. Padrão: ./MegaMan3.nes")
    print("  --sequencia=<sequencia>:")
    print("       (1,2,3,...8) Sequência de fases a ser seguida.")
    print("       Números separados por vírgula. Caso seja omitido, será")
    print("       sequencial de 1 a 8.")
    print("  --carregar-pre:")
    print("       Carrega um estado pré carregado do emulador. Padrão: False")
    print("  --fceux=<caminho>:")
    print("       Caminho para o executavél do emulador fceux. Padrão: /usr/games/fceux")
    print("  --fceux_script=<caminho>:")
    print("       Caminho para o script lua 'servidor'. Padrão: ./server.lua")
    print("")
    exit(3)


def treinamento(params):
    """Verifica os parâmetros para treinamento e
    inicia com as opções recebidas"""
    
    if not params.validarTreinamento():
        exit(3)
    
    treino = megaman_ai.treinamento.Treinamento(
        videos=params.videos,
        sprites=params.sprites,
        destino=params.destino,
        skip=params.skip,
        exibir=params.exibir,
        tempo=params.tempo,
        qualidade=params.qualidade,
        historico=params.historico)
    
    treino.iniciar()


def jogar(params):
    """Verifica os parâmetros para jogar e
    inicia com as opções recebidas"""

    if not params.validarJogar():
        exit(3)
    
    jogo = megaman_ai.jogo.Jogo(
        room = params.room,
        sequencia = params.sequencia, 
        carregar_pre = params.carregar_pre,
        fceux=params.fceux,
        fceux_script=params.fceux_script)
    
    jogo.iniciar()

if __name__ == "__main__":
    # Recebe parâmetros via linha de comando
    try:
        params = megaman_ai.parametros.parse()
    except Exception as erro:
        print(erro)
        uso() # exit

    # Exibe informações de ajuda se for necessário
    if params.ajuda: 
        uso() # exit
    
    # Modo treinameto
    if params.treinamento:
        treinamento(params)
    
    # Modo jogar
    else:
        jogar(params)
