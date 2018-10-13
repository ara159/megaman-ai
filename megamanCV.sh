#!/bin/bash
escala=$1
if [ -z $1 ]; then escala=2; fi

nestopia -d Arquivos/MegaMan3.nes -s $escala > /dev/null &
python3 megamanCV.py $escala