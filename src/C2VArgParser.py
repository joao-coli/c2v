import sys
import argparse # Módulo do python para parsing de argumentos de linha de comando

class C2VArgParser:
  def __init__(self):
    # Parser principal para o programa C2V
    self.arg_parser = argparse.ArgumentParser(description='Parser de argumentos do shell')
    self.subparsers = self.arg_parser.add_subparsers(dest='comando') # Variável para a criação de subparsers

    # Subparser para o comando 'ajuda'
    self.ajuda_parser = self.subparsers.add_parser('ajuda', description='Parser para o subcomando de ajuda',
                                                    help="Exibe as informações de utilização do programa")

    # Subparser para o comando 'analisar'
    self.analisar_parser = self.subparsers.add_parser('analisar', description='Parser para o subcomando de análise de código',
                                        help=("Dado um arquivo de entrada contendo o código na linguagem C2V, "
                                          "executa as análisdes léxica, sintática e semântica a fim de "
                                          "validar o código do arquivo."))
    self.analisar_parser.add_argument('-e', '--entrada', type=str, nargs=1, help=("Caminho para o arquivo de entrada "
                                                                      "contendo o programa na linguagem C2V."),
                                                                      required=True)

    # Subparser para o comando 'gerar'
    self.gerar_parser = self.subparsers.add_parser('gerar', description='Parser para o subcomando de geração de código', 
                                     help=("Dada um arquivo de entrada contendo código na linguagem C2V, "
                                      "gera um arquivo HTML com nome e localização definidos pelo"
                                      "parâmetro de saída."))
    self.gerar_parser.add_argument('-e', '--entrada', type=str, nargs=1, help=("Caminho para o arquivo de entrada "
                                                                      "contendo o programa na linguagem C2V."),
                                                                      required=True)
    self.gerar_parser.add_argument('-s', '--saida', type=str, nargs=1, help=("Caminho para o arquivo de saída que"
                                                                    "irá conter o código HTML gerado."),
                                                                    required=True)

  def parse_args(self):
    return self.arg_parser.parse_args()
