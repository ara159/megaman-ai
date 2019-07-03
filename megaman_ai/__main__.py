import megaman_ai

# TODO: Acrecentar intrução de como entrar no modo jogar
def uso():
    print("Megaman AI")
    print("")
    print("Trabalho de TCC - Rafael Costa e Robson Santos")
    print("")
    print("O objetivo do projeto é criar uma inteligência artificial")
    print("capaz de jogar pelo menos uma fase de MegaMan3.")
    print("")
    print("Uso:")
    print("  python3 -m megaman_ai [opções]")
    print("")
    print("Opções Gerais:")
    print("  --ajuda:")
    print("       Exibe esta mensagem de ajuda.")
    print("  --treinamento <videos>:")
    print("       Executa no modo treinamento.")
    print("       Quando neste modo, é necessário se passar os videos")
    print("       que serão usados no treinamento.")
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
    print("  --manter:")
    print("       Mantém a tela do game focada durante a execução.")
    print("  --sequencia=<sequencia>:")
    print("         (1,2,3,...8) Sequência de fases a ser seguida.")
    print("         Números separados por vírgula. Caso seja omitido, será")
    print("         sequencial de 1 a 8.")
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
    
    # megaman_ai.jogar(
    #     room = "MegaMan3.nes", # TODO: Parametrizar
    #     sequencia = params.sequencia, 
    #     focar = params.manter,
    #     carregar = params.carregar_pre,
    #     foco_tx = 0.3, # TODO: Parametrizar
    #     escala = 2, # TODO: Parametrizar
    #     exibir = False) # TODO: Parametrizar

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
