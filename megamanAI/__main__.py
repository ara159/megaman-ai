import megamanAI

# room: "arquivos/MegaMan3.nes"
# tempo de manutenção tela: 0.3

def ini_teste(room, sequencia_fases=[], focar_tela=True, atualizacao_tela=0.3, debug=False, escala=2):
    e = megamanAI.emulador.Emulador(room, escala=escala)
    m = megamanAI.emulador.ManterEmulador(e, atualizacao_tela)
    m3 = megamanAI.MegaMan3(e)

    # inicia as threads do emulador e de manutenção da janela
    e.start()
    if focar_tela:
        m.start()

    m3.iniciar(debug) # se debug entra carregando estado pré carregado

    if debug: m3.jogar()

    else:
        for i in sequencia_fases:
            m3.escolher_fase(i)
            m3.jogar()

# TODO: Implementar suporte a escala maiores
ini_teste("arquivos/MegaMan3.nes", sequencia_fases=[1], focar_tela=True, debug=True, escala=1)
