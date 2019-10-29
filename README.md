# MEGAMAN-AI
Megaman-ai é uma inteligencia artificial que aprende a jogar `Megaman 3` a partir de vídeos!

## Quickstart

### Clonar o projeto
```
git clone https://github.com/ara159/megaman-ai && cd megaman-ai
```
### Instalar pré requisitos
```
# Lua
sudo apt-get install lua5.2 lua-socket lua-json 

# Emulador fceux
sudo apt-get install fceux

# Python >= 3.6
sudo apt-get install python3
```
### Instalar os requerimentos do python
```
pip3 install -r requirements.txt
```
### Criar um modelo
```
python3 exemplo.py
```
### Iniciar treinamento
```
python3 --treinamento --nome exemplo --time_steps 15 --epochs 10 videos/exemplo.mp4
```
### Jogar
```
sudo python3 --nome exemplo --time_steps 15
```

## Como usar?
Para começar é necessário criar um modelo de rede neural para o treinamento. Cada modelo criado deverá ter um nome. Os modelos ficam armazenados na pasta `modelos`.

O programa no geral tem dois modos: `Treinar` e `Jogar`. Ao usar qualquer um dos modos, um modelo deve ser especificado, juntamente com o `time steps` que ela executa.

Claro que se você criar um modelo e mandar ele jogar sem treinar, não vai dar muito certo. O ideal é criar a rede, treinar e depois mandar jogar.

No processo de treinamento, o programa salva os resultados do treinamento em arquivos de log em formato `yaml` que ficam na pasta `logs`. Esses arquivos podem ser analisados depois com o programa `analise.py` ou você pode criar seu próprio programa para analisar se quiser. Nesses arquivos ficam todo o histórico de aprendizado de um modelo.

Ao interromper o treinamento o modelo é salvo. Porém quando for treinar de novo, o vídeo será lido des de o inicio. Portanto não é recomendado interromper o treinamento, visto que pode gerar overfiting.

No modo jogar, a cada ação que o modelo toma gera uma saída no console mostrando a decisão tomada e a porcentagem de certeza da decisão.

Lembrando que a IA só vai se sair bem caso seja bem treinada. E para ser bem treinada, deve se ter um cuidado e preparo em cada parte do processo. Isso inclui o vídeo que será usado para treinar, o modelo criado, os parâmetros de treinamento e o monitoramento da evolução.

## Parâmetros
Tem 3 tipos de parâmetros, os `gerais`, que podem ser usados *nos dois modos do programa*, os de `treinamento`, que só são válidos no *modo treinamento*, e os de `jogar`, que só são válidos no *modo jogar*.

### Gerais
* --config <str>
  
Especifica um arquivo de configurações. 
As configurações do arquivo são as mesmas da linha de comando.

* --time_steps <int>
  
Em redes recorrentes, o número de frames analisados usados na tomada de decisão.

* --nome <str>
  
O nome do modelo a ser usado. 

* --sprites <str>
  
Arquivo com as defições sobre sprites.

* --fps <int>
  
FPS ao ser usado. O ideal é, para um modelo, usar o mesmo fps, tanto para treinar tanto para jogar. Os valores aceitos são: 30, 15, 10, 5.

### Treinamento
* --frames

A quantidade de frames a ser analisados de uma só vez por época.

* --epochs <int>
  
Quantidade de épocas de treinamento.

* --batch_size <int>
  
O tamanho do batch dentro de uma época.

* --nthreads <int>
  
Quantidade de threads usadas no treinamento. Se estiver treinando uma rede recorrente este valor deve ser 1.

* --suffle

Se os exemplos devem ser misturados aleatoriamente antes de começar treinar.

### Jogar
* --room <str>
  
Caminho da room a ser usada.
  
* --fceux <str>
  
Caminho do executável do emulador fceux.

* --fceux_script <str>
  
Caminho do script lua a ser executado junto ao emulador. O script é o `lua/server.lua`.
