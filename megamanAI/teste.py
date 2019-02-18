import emulador, mega, cv

# room: "arquivos/MegaMan3.nes"
# tempo de manutenção tela: 0.3

def ini_teste(room, sequencia_fases=[], focar_tela=True, atualizacao_tela=0.3, debug=False, escala=2):
    e = emulador.Emulador(room, escala=escala)
    m = emulador.ManterEmulador(e, atualizacao_tela)
    c = emulador.Controle(e)
    m3 = mega.MegaMan3(e, c)
    
    # inicia as threads do emulador e de manutenção da janela
    e.start()
    if focar_tela: m.start()

    m3.iniciar_game(debug) # se debug entra carregando estado pré carregado

    if debug:
        cv.jogar_fase(e)
    else:
        for i in sequencia_fases:
            m3.escolher_fase(i)
            cv.jogar_fase(e)

# TODO: Implementar suporte a escala maiores
ini_teste("arquivos/MegaMan3.nes", sequencia_fases=[1], focar_tela=True, debug=True, escala=1)