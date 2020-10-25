from textx import metamodel_from_file
from src.C2VSintatico import C2VSintatico
from src.C2VSemantico import C2VSemantico
from src.C2VGerador import C2VGerador
from inspect import getmembers # Para debug
from pprint import pprint # Para debug
import sys
import argparse # Módulo do python para parsing de argumentos de linha de comando


class C2V:
  saida = []
  gramatica = "src/c2v.tx"

  def __init__(self, arquivo):
    """
    @arquivo: caminho para o arquivo com o programa
    """
    self.arquivo = arquivo
    self.meta_modelo = metamodel_from_file(self.gramatica) # Criação da árvore da linguagem


  def analisar(self):
    """
    Realiza as análises sintática e semântica.
    Retorna as variáveis definidas se a análise foi bem sucedida (sem erros) ou 'False', do contrário (encontrou erros).
    """
    sintatico = C2VSintatico(self.meta_modelo)
    self.modelo = sintatico.analisar(self.arquivo) # Análise sintática

    semantica = False
    if self.modelo: # Caso a análise sintática tenha de fato retornado um modelo (e não 'False')
      semantico = C2VSemantico(self.modelo)
      semantica = semantico.analisar()

    if semantica:
      print("Análise realizada com sucesso.")
      return semantico.variaveis
    else:
      print("Análise finalizada com erros.")
      return False

  
  def gerar(self):
    variaveis = self.analisar()

    if variaveis:
      gerador = C2VGerador(variaveis)
      gerador.gerar()
      print("Fim da compilação.")
    else:
      print("Falha na compilação.")
      # Análise com erros; não há nada a ser gerado


# Parser principal para o programa C2V
arg_parser = argparse.ArgumentParser(description='Parser de argumentos do shell')
subparsers = arg_parser.add_subparsers(dest='comando') # Variável para a criação de subparsers

# Subparser para o comando 'ajuda'
ajuda_parser = subparsers.add_parser('ajuda', description='Parser para o subcomando de ajuda',
                                    help="Exibe as informações de utilização do programa")

# Subparser para o comando 'analisar'
analisar_parser = subparsers.add_parser('analisar', description='Parser para o subcomando de análise de código',
                                        help=("Dado um arquivo de entrada contendo o código na linguagem C2V, "
                                          "executa as análisdes léxica, sintática e semântica a fim de "
                                          "validar o código do arquivo."))
analisar_parser.add_argument('-e', '--entrada', type=str, nargs=1, help=("Caminho para o arquivo de entrada "
                                                                      "contendo o programa na linguagem C2V."),
                                                                      required=True)

# Subparser para o comando 'gerar'
gerar_parser = subparsers.add_parser('gerar', description='Parser para o subcomando de geração de código', 
                                     help=("Dada um arquivo de entrada contendo código na linguagem C2V, "
                                      "gera um arquivo HTML com nome e localização definidos pelo"
                                      "parâmetro de saída."))
gerar_parser.add_argument('-e', '--entrada', type=str, nargs=1, help=("Caminho para o arquivo de entrada "
                                                                      "contendo o programa na linguagem C2V."),
                                                                      required=True)
gerar_parser.add_argument('-s', '--saida', type=str, nargs=1, help=("Caminho para o arquivo de saída que"
                                                                    "irá conter o código HTML gerado."),
                                                                    required=True)

#arg_parser.add_argument('ajuda', help="Imprime na tela a lista de comandos disponíveis")
args = arg_parser.parse_args()

print(args)
    
#c2v = C2V('c2v.c2v')
#c2v.gerar()

