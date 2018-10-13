#!/bin/bash
escala=$1
if [ -z $1 ]; then escala=2; fi

nestopia -d Arquivos/MegaMan3.nes -s $1 &
python3 megamanCV.py $1