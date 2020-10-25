from textx import metamodel_from_file
from src.C2VSintatico import C2VSintatico
from src.C2VSemantico import C2VSemantico
from src.C2VGerador import C2VGerador
from src.C2VArgParser import C2VArgParser
from inspect import getmembers # Para debug
from pprint import pprint # Para debug
import sys
import os
import argparse # Módulo do python para parsing de argumentos de linha de comando


class C2V:
  gramatica = "src/c2v.tx"

  def __init__(self, argumentos):
    """
    @argumentos: argumentos do terminal interpretados
    """
    self.args = argumentos


  def executar(self):
    comando = self.args.comando

    if comando == 'analisar' or comando == 'gerar':
      self.arquivo = self.args.entrada[0]
      self.meta_modelo = metamodel_from_file(self.gramatica)

      if comando == 'analisar':
        self.analisar()
      else: # Senão, é o subcomando 'gerar'
        self.saida = self.args.saida[0]
        self.gerar()
    elif comando == 'testar':
      self.meta_modelo = metamodel_from_file(self.gramatica)

      if self.args.sintatico:
        caminho = "casos_de_teste/erros_sintaticos/"
        print("---------------- Análise Sintática ---------------- ")
        for arquivo in os.listdir(caminho):
          print(f"------ {arquivo} ------")
          self.arquivo = os.path.join(caminho, arquivo)
          self.analisar()
          print("")

      if self.args.semantico:
        caminho = "casos_de_teste/erros_semanticos/"
        print("---------------- Análise Semântica ---------------- ")
        for arquivo in os.listdir(caminho):
          print(f"------ {arquivo} ------")
          self.arquivo = os.path.join(caminho, arquivo)
          self.analisar()
          print("")

      if self.args.geracao:
        caminho = "casos_de_teste/corretos/"
        print("---------------- Geração de código ---------------- ")
        for arquivo in os.listdir(caminho):
          print(f"------ {arquivo} ------")
          self.arquivo = os.path.join(caminho, arquivo)
          self.saida = os.path.join('saida/corretos/', (arquivo+'.html'))
          self.gerar()
          print("")

    elif comando == 'ajuda':
      print(
        f"Comandos disponíveis:\n"
        f"\t ajuda\n"
        f"\t\t Descrição: imprime esta tela de ajuda\n\n"
        f"\t analisar -e/--entrada\n"
        f"\t\t Descrição: dado um caminho para um arquivo de entrada (fornecido pela flag -e/--entrada),\n"
        f"\t\t realiza as análises léxica, sintática e semântica no código C2V do arquivo de entrada\n\n"
        f"\t gerar -e/--entrada -s/--saida\n"
        f"\t\t Descrição: dado um caminho para um arquivo de entrada (fornecido pela flag -e/--entrada)\n"
        f"\t\t e um caminho para um arquivo de saída (fornecido pela flag -s/--saida), realiza as análises\n"
        f"\t\t léxica, sintática, semântica e, se todas passarem, gera o código HTML no arquivo de saída\n\n"
        f"\t testar [--sintatico] [--semantico] [--geracao]\n"
        f"\t\t Descrição: executa os casos de testes definidos em 'casos_de_teste' de acordo com a flag\n"
        f"\t\t informada (todas são opcionais). Por exemplo, usar a flag --semantico executaria os casos\n"
        f"\t\t de teste com erros semânticos.\n\n"
        f"\t Adicionar -h antes de cada subcomando traz informações adicionais."
      )


  def analisar(self):
    """
    Realiza as análises sintática e semântica.
    Retorna as variáveis definidas se a análise foi bem sucedida (sem erros) ou 'False', do contrário (encontrou erros).
    """
    self.modelo = False # Reiniciando caso já tenha sido executado

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
      gerador = C2VGerador(variaveis, self.saida)
      gerador.gerar()
      print("Fim da compilação.")
    else:
      print("Falha na compilação.")
      # Análise com erros; não há nada a ser gerado


# Parser de linha de comando
arg_parser = C2VArgParser()
args = arg_parser.parse_args() # Variável que irá conter os argumentos passados
    
# Classe de controle do pipeline para a linguagem C2V
c2v = C2V(args)
c2v.executar()

