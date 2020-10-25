from .Analisador import AnalisadorSemantico
import os
from pprint import pprint # Para debug


class C2VSemantico(AnalisadorSemantico):
  variaveis = {} # Dicionário que irá guardar as definições e seus valores 
                 # Tabela de símbolos simplificada, pois não há escopos distintos
  ATRIBUTOS = ['titulo', 'codigo' , 'imagem', 'preco', 'descricao', 'pagamentos',
               'loja', 'avaliacoes', 'lojas', 'sugestoes'] # Todos os atributos
  OBRIGATORIOS = ['loja', 'titulo', 'preco', 'descricao'] # Atributos obrigatórios

  def __init__(self, modelo): # Espera receber um modelo do textX para a linguagem C2V
    self.modelo = modelo
    self.parser = self.modelo._tx_parser # Recuperando o parser do modelo


  def verificarTipo(self, atributo, argumento, linha):
    NUMERICOS = ['preco', 'codigo', 'nota', 'desconto', 'ate', 'de', 'parcela'] # Espera um número
    IMAGEM = ['imagem'] # Espera uma string contendo um caminho para um arquivo
    URL = ['site'] # Espera uma string contendo uma url válida
    EXTENSOES_IMAGEM = ['jpg', 'jpeg', 'png', 'bmp', 'svg']

    # O argumento pode ser um número (INT | FLOAT) ou uma string (str, no Python)
    if atributo in NUMERICOS and isinstance(argumento, str):
      self.mostrarErro(f"'{atributo}' deve receceber um número", linha)
      return False
    elif atributo not in NUMERICOS and not isinstance(argumento, str):
      self.mostrarErro(f"'{atributo}' deve receber uma cadeia de caracteres", linha)
      return False
    elif atributo in IMAGEM:
      if not os.path.isfile(argumento): # Não é um caminho válido para um arquivo
        self.mostrarErro(f"'{atributo}' deve receber um caminho para uma imagem", linha)
        return False
      
      # Neste ponto, sabe-se que o argumento representa o arquivo. Falta validar a extensão
      diretorios = argumento.split('/') # Divisão por diretórios (a última entrada é o nome do arquivo)
      arquivo = diretorios[len(diretorios) - 1].split('.') # A última entrada é a extensão (quando houver)

      if not (arquivo[len(arquivo) - 1] in EXTENSOES_IMAGEM):
        self.mostrarErro(f"'{atributo}' deve receber uma imagem de uma das seguintes extensões: {', '.join(EXTENSOES_IMAGEM)}.", linha)
        return False

    return True

  
  def analisar(self):
    no_errors = True

    for cmd in self.modelo.comandos: # Análises retornam 'True' se não houve erros, e 'False' caso tenha ocorrido algum
      no_errors = self.analisarComando(cmd) and no_errors # Esta disposição força a análise a sempre ser executada

    # Subtração de conjuntos: obrigatorios_faltantes deve conter os comandos obrigatórios que não estão presentes
    #       no conjunto de comandos (isto é, não foram usados)
    obrigatorios_faltantes = set(self.OBRIGATORIOS) - set(self.variaveis.keys())
    if obrigatorios_faltantes:
      # Um erro deve ser mostrado para cada caso      
      for var in obrigatorios_faltantes:
        self.mostrarErroNaoDeclarado(var)

      no_errors = False
    
    if no_errors: # Nenhum erro encontrado
      # Opcionais: (ATRIBUTOS - OBRIGATÓRIOS) - JÁ DEFINIDOS
      opcionais = list((set(self.ATRIBUTOS) - set(self.OBRIGATORIOS)) - set(self.variaveis.keys()))

      for var in opcionais:
        self.variaveis[var] = "" # Define-se uma string vazia

    return no_errors

  
  def analisarComando(self, Comando):
    nome_classe = type(Comando).__name__
    res = True

    # Sempre será um dos dois
    if nome_classe == "ComandoDefina":
      res = self.analisarComandoDefina(Comando)
    elif nome_classe == "ComandoListe":
      res = self.analisarComandoListe(Comando)

    return res


  def analisarComandoDefina(self, Comando):
    """
    Verifica se o atributo a ser definido recebeu um tipo corrreto
    """
    NUMERICOS = ['preco', 'codigo']
    linha, coluna = self.parser.pos_to_linecol(Comando._tx_position) # Linha e coluna da ocorrência
    
    if Comando.tipo in self.variaveis: # Tipo já foi previamente definido
      self.mostrarErroJaDeclarado(Comando.tipo, linha)
      return False

    tipo_correto = self.verificarTipo(Comando.tipo, Comando.argumento, linha)
    if not tipo_correto:
      return False # Erro já foi mostrado neste ponto

    self.variaveis[Comando.tipo] = Comando.argumento # Salvando a variável
    return True

  
  def analisarComandoListe(self, Comando):
    tipo = Comando.tipo
    res = True
    lista = []
    funcoes = {
      'avaliacoes': self.analisarAvaliacao,
      'lojas': self.analisarLoja,
      'sugestoes': self.analisarSugestao,
      'pagamentos': self.analisarPagamento
    }

    linha, coluna = self.parser.pos_to_linecol(Comando._tx_position) # Linha e coluna da ocorrência

    if tipo in self.variaveis: 
      self.mostrarErroJaDeclarado(tipo, linha)
      res = False
      # A análise não será interrompida, permitindo as análises posteriores

    for elemento in Comando.lista:
      aux = funcoes[tipo](elemento, lista) # Chama a função salva no dicionário de função para o respectivo elemento

      if not aux: # aux é 'False', e não uma entrada válida
        res = False
        continue

      lista.append(aux) #Se retornou uma entrada válida, é adicionada à lista auxiliar

    if res:
      self.variaveis[tipo] = lista

    return res


  def analisarAvaliacao(self, Avaliacao, lista_atual):
    linha, coluna = self.parser.pos_to_linecol(Avaliacao._tx_position) # Linha e coluna da ocorrência

    if not type(Avaliacao).__name__ == 'Avaliacao': # Não é uma avaliação
      self.mostrarErro(f"a entrada fornecida não está no formato esperado para uma avaliação", linha)
      return False

    nota = self.verificarTipo('nota', Avaliacao.nota, linha)
    descricao = self.verificarTipo('descricao', Avaliacao.descricao, linha)
    autor = self.verificarTipo('autor', Avaliacao.autor, linha)

    if not (nota and descricao and autor): # Se pelo menos uma das verificações encontrou um problema
      return False # Erros já foram tratados nesta etapa

    if Avaliacao.nota > 10 or Avaliacao.nota < 0: # Fora dos limites esperados
      self.mostrarErro(f"a nota de uma avaliação deve estar entre 0 e 10", linha)
      return False

    return { 'nota': Avaliacao.nota, 'descricao': Avaliacao.descricao, 'autor': Avaliacao.autor }


  def analisarLoja(self, Loja, lista_atual):
    linha, coluna = self.parser.pos_to_linecol(Loja._tx_position) # Linha e coluna da ocorrência

    if not type(Loja).__name__ == 'Loja': # Não é uma loja
      self.mostrarErro(f"a entrada fornecida não está no formato esperado para uma loja", linha)
      return False

    nome = self.verificarTipo('nome', Loja.nome, linha)
    site = self.verificarTipo('site', Loja.site, linha)

    if not (nome and site): # Se pelo menos uma das verificações encontrou um problema
      return False # Erros já foram tratados nesta etapa

    # TODO: averiguar URLs para os sites

    return { 'nome': Loja.nome, 'site': Loja.site }


  def analisarSugestao(self, Sugestao, lista_atual):
    linha, coluna = self.parser.pos_to_linecol(Sugestao._tx_position) # Linha e coluna da ocorrência

    if not type(Sugestao).__name__ == 'Sugestao': # Não é uma sugestão
      self.mostrarErro(f"a entrada fornecida não está no formato esperado para uma sugestão", linha)
      return False

    produto = self.verificarTipo('produto', Sugestao.produto, linha)
    preco = self.verificarTipo('preco', Sugestao.preco, linha)

    if not (produto and preco): # Se pelo menos uma das verificações encontrou um problema
      return False # Erros já foram tratados nesta etapa

    if Sugestao.preco < 0:
      self.mostrarErro(f"o produto sugerido não pode ter um preço negativo", linha)
      return False

    return { 'produto': Sugestao.produto, 'preco': Sugestao.preco }


  def analisarPagamento(self, Pagamento, lista_atual):
    linha, coluna = self.parser.pos_to_linecol(Pagamento._tx_position) # Linha e coluna da ocorrência

    if not type(Pagamento).__name__ in ['AVista', 'Parcelado']: # Não é um modo de pagamento
      self.mostrarErro(f"a entrada fornecida não está no formato esperado para um modo de pagamento", linha)
      return False

    modo = Pagamento.modo # Modo de pagamento de acordo com a string

    # Este erro é tratado aqui pois, se fosse pelo analisador sintático, seria mostrada uma
    #   mensagem genérica. Aqui, pode-se mostrar algo mais explicativo ao usuário
    for elemento in lista_atual:
      if elemento['modo'] == modo: # Modo de pagamento já declarado anteriormente
        self.mostrarErroJaDeclarado(modo, linha)
        return False

    res = False
    if modo == 'a vista':
      res = self.analisarAVista(Pagamento)
    else:
      res = self.analisarParcelado(Pagamento)

    return res


  def analisarAVista(self, Pagamento):
    linha, coluna = self.parser.pos_to_linecol(Pagamento._tx_position) # Linha e coluna da ocorrência
    valor_desconto = Pagamento.desconto

    # Se não foi definido um desconto, ele é zero
    if valor_desconto is None:
      valor_desconto = 0

    desconto = self.verificarTipo('desconto', valor_desconto, linha)

    if not desconto:
      return False # Erro já foi tratado na verificação de tipo

    if valor_desconto < 0 or valor_desconto > 100:
      self.mostrarErro(f"o desconto deve ser um número entre 0 e 100 (indicando percentual)", linha)
      return False

    return { 'modo': Pagamento.modo, 'desconto': round(valor_desconto, 2) }


  def analisarParcelado(self, Pagamento):
    linha, coluna = self.parser.pos_to_linecol(Pagamento._tx_position) # Linha e coluna da ocorrência
    de_minimo, ate_maximo = Pagamento.minimo, Pagamento.maximo

    if de_minimo is None: # Assume-se que a menor quantidade de parcelas seja 2, caso não informado
      de_minimo = 2 # Apenas uma parcela seria o mesmo que à vista

    minimo = self.verificarTipo('de', de_minimo, linha) 
    maximo = self.verificarTipo('ate', ate_maximo, linha)

    if not (minimo and maximo):
      return False # Erros já foram tratados na verificação de tipos

    if not (isinstance(de_minimo, int) and isinstance(ate_maximo, int)):
      self.mostrarErro("os valores de quantidade de parcelas devem ser números inteiros", linha)
      return False

    if de_minimo <= 1:
      self.mostrarErro("o valor mínimo de parcelas deve ser maior que um", linha)

    if ate_maximo <= 0:
      self.mostrarErro("o valor máximo de parcelas devem ser maior que zero", linha)
      return False

    if de_minimo > ate_maximo:
      self.mostrarErro("o valor mínimo de parcelas não pode exceder o máximo", linha)
      return False

    return { 'modo': Pagamento.modo, 'de': de_minimo, 'ate': ate_maximo }