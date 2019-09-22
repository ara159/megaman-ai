socket = require("socket.core")
json = require("json")

sock, err = socket.tcp()

if sock then
    sock:setoption("reuseaddr", true)
    e, a = sock:bind("127.0.0.1", 4321)
    if a then 
        print(e, a)
        os.exit() 
    end
    e, a = sock:listen(1)
end

print("Lua: Aguardando conexão...")

client = sock:accept()
client:settimeout(10)

print("Lua: Cliente conectado")

-- Carrega a fase
ss = savestate.create(1)
savestate.load(ss)

proximo = true

while true do
    if proximo then
        -- Tira screenshot do frame
        gui.savescreenshotas("/tmp/.megamanAI.screen")
        
        -- Envia confirmação de pronto para recebimento
        -- de comandos
        client:send("Pronto")
        
        -- trava
        proximo = false

        -- Avança um frame
        emu.frameadvance()
    end
    
    -- Aguarda comando relativo ao ultimo frame salvo
    line, err = client:receive()

    -- quando receber algo
    if line then

        -- Executa a ação
        atual = json.decode(line)
        joypad.set(1, atual)
        proximo = true
    end
end
