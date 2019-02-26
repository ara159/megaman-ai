from megaman_ai import emulador, megaman3, coleta

def jogar(room, 
            config,
            sequencia  = [], 
            focar      = True, 
            foco_tx    = 0.3, 
            carregar   = False, 
            escala     = 1,
            exibir     = False):
    
    emu = emulador.Emulador(
            room    = room, 
            posicao = (config.video["left"],config.video["top"]), 
            escala  = escala)

    foco = emulador.ManterEmulador(
            emulador = emu,
            taxa     = foco_tx)

    megaman = megaman3.MegaMan3(emulador=emu)

    if not focar:
        foco.taxa = -1

    emu.start()
    foco.start()
    
    if carregar: 
        megaman.carregar()
        megaman.jogar(exibir=exibir)
    else:
        megaman.iniciar()
        for fase in sequencia:
            megaman.escolher_fase(fase)
            megaman.jogar(exibir=exibir)
    
    print("Fim Thread principal")