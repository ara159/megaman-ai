"""
parametros.py

Funções para tratamento dos parâmetros recebidos via
linha de comando.
"""

from sys import argv
from getopt import getopt

class Parametros:
    """ 
    Parâmetros
    ==========
    Armazena as opções recebidas pelo usuário via linha de comando
    para a execução do programa.
    Os atributos já iniciam com os valores padrão.
    A lista de parâmetros é criada a partir dos atributos da classe.
    """
    treinamento = False
    exibir = False
    config = ""
    ajuda = False
    carregar_pre = False
    manter = False
    sequencia = list(range(1, 10))
    qualidade = False
    tempo = False
    skip = 0
    destino = ""

    def __init__(self, opts):
        self.parse(opts)

    def parse(self, opts):
        """Preenche o objeto com as opções recebidas"""
        # Configura os parâmetros que são esperados
        for parametro, valor in opts[0]:
            if "--" in parametro and len(valor) == 0:
                setattr(self, parametro[2:], True)
            else:
                self.__setattr__(parametro[2:], valor)
        
        self.sequencia = list(map(int, self.sequencia.split(',')))
        # Configura os valores extras de parâmetro

    @staticmethod
    def getopts():
        """Recupera a lista de objetos que podem ser recebidos
        por parâmetro do usuário, a lista é gerada baseada nos
        atributos da classe"""
        opts = []
        for attr in Parametros.__dict__.keys():
            if "__" in attr:
                continue
            
            tipoattr = type(getattr(Parametros, attr))
            
            if tipoattr.__name__ == "function":
                continue
            
            if tipoattr.__name__ == "bool":
                opts.append(attr)
            else:
                opts.append(attr+"=")

        return opts

def parse():
    """Cria, preenche e retorna um objeto `Parametro`"""
    # TODO: Verificar a necessidade de se ter parâmetros curtos
    opts_curta = ""
    opts_longa = Parametros.getopts()
    args = ["--sequencia=1,2,3", "--exibir"]
    opts = getopt(args, opts_curta, opts_longa)
    parametros = Parametros(opts)
    return parametros