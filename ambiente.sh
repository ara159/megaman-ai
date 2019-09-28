#!/bin/bash

proxy(){
    echo -n "Endereço do proxy (com a porta): "
    read PXY_ADDR
    echo -n "Usuário proxy: "
    read PXY_USER
    echo -n "Senha: "
    read -s PXY_PASS

    PROXY="http://$PXY_USER:$PXY_PASS@$PXY_ADDR"

    # Configura git
    git config --global http.proxy $PROXY
    git clone https://github.com/ara159/megaman-ai
    cd megaman-ai
    git checkout origin/mutithread

    # Instala dependencias
    pip3 install -r requirements.txt --proxy $PROXY
}

normal(){
    # Configura git
    git clone https://github.com/ara159/megaman-ai
    cd megaman-ai
    git checkout origin/mutithread

    # Instala dependencias
    pip3 install -r requirements.txt
}

if [ "$1" == "--proxy" ]
then
    proxy
else
    normal
fi
