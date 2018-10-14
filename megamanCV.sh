#!/bin/bash
escala=$1
if [ -z $1 ]; then escala=2; fi

nestopia -d arquivos/MegaMan3.nes -s $escala 2> /dev/null &
python3 megamanCV.py $escala