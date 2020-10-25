import os

class C2VGerador:
  
  def __init__(self, variaveis):
    self.variaveis = variaveis
  

  def gerar(self):
    """
    Cria o arquivo HTML de saída com base nas variáveis retiradas de um modelo da linguagem C2V
    """

    # Usa-se o 'os.path.dirname' para se identificar corretamente o caminho até a pasta 'src/'
    # Por padrão, o python atribui os caminhos relativos como sendo iniciados no caminho para o primeiro script executado
    # No caso, mesmo nesse arquivo, os caminhos relativos são para a pasta anterior, pois excecuta-se somente 'c2v.py'
    with open(os.path.join(os.path.dirname(__file__), "template.html")) as html_file:
      html = html_file.read()
      for var in self.variaveis.keys(): # Iterando sobre o dicionário (var recebe as chaves do dicionário)
        html = html.replace("{{ " + var + " }}" , self.traduzirParaHTML(var, self.variaveis[var]))

      final = open('final.html', 'w') # Caminho relativo salvará na pasta raiz do projeto
      final.write(html)

  def traduzirParaHTML(self, tipo, valor):
    """
    Retorna uma string contendo o código HTML para a variável
    @tipo: nome da variável
    @valor: valor da variável no modelo
    """

    final = str(valor) # Algumas variáveis não requerem tratamento. Basta o valor originalmente passado

    #print('atributo = ', tipo, ' e valor = ', valor)

    if tipo == "preco":
      final = self.traduzirPreco(valor)
    elif tipo == "codigo":
      final = self.traduzirCodigo(valor)
    elif tipo == "imagem":
      final = self.traduzirImagem(valor)
    elif tipo == "sugestoes":
      final = self.traduzirSugestoes(valor)
    elif tipo == "lojas":
      final = self.traduzirLoja(valor)
    elif tipo == "avaliacoes":
      final = self.traduzirAvaliacoes(valor)
    elif tipo == "pagamentos":
      final = self.traduzirPagamentos(valor)

    return final


  def traduzirImagem(self, valor):
    """
    Retorna uma string contendo o código HTML para a imagem
    @valor: espera um caminho válido para uma imagem ou uma string vazia (indicando que não há imagem)
    """
    if valor == "": # Não foi informado o caminho para uma imagem 
      return "<h3 class='sem-imagem'>Sem imagem</h3>"

    return f"<img src='{valor}'></img>"
  

  def traduzirPreco(self, valor):
    """
    Retorna uma string contendo o código HTML para o preço
    @valor: espera um número (INT ou FLOAT)
    """

    # Usa-se 'float' para forçar o número em ponto flutuante, mesmo que seja um INT
    # TODO: possibilitar outras moedas
    return f"<b>R${round(float(valor), 2):.2f}</b>" # ':.2f' -> força duas casas decimais


  def traduzirCodigo(self, valor):
    """
    Retorna uma string contendo o código HTML para o preço
    @valor: espera uma string contendo o código ou uma string vazia
    """
    codigo = valor if len(valor) > 0 else "--"
    return codigo


  def traduzirLoja(self, lojas):
    """
    Retorna uma string contendo o código HTML para as sugestões
    @lojas: espera uma lista de dicionários contendo lojas parceiras
    """
    if lojas == "" or not len(lojas):
      return "<h3 class='no-margin-heading padding-5'>Sem lojas parceiras</h3>"


    final = []
    divisor = "<hr class='divisor-horizontal'>"

    for loja in lojas:
      # Notação do Python para strings em múltiplas linhas.
      # Utilizada para se manter a hierarquia do HTML
      final.append(
        f"<div id='loja' class='padding-5'>"
          f"<a id='link-loja' href='{loja['site']}'><h4 class='no-margin-heading'>{loja['nome']}</h4></a>"
        f"</div>"
      )

    return divisor.join(final)


  def traduzirSugestoes(self, sugestoes):
    """
    Retorna uma string contendo o código HTML para as sugestões
    @sugestoes: espera uma lista de dicionários contendo produtos sugeridos
    """
    if sugestoes == "" or not len(sugestoes):
      return f"<h3 class='sem-sugestoes padding-5'>{self.variaveis['loja']}</h3>"

    final = []
    divisor = "<hr class='divisor-vertical'>"

    for produto in sugestoes:
      # Notação do Python para strings em múltiplas linhas.
      # Utilizada para se manter a hierarquia do HTML
      final.append(
        f"<div class='sugestao'>"
          f"<h3 class='no-margin-heading padding-5'>"
            f"{produto['produto']}"
          f"</h3>"
          f"<div>"
            f"{self.traduzirPreco(produto['preco'])}"
          f"</div>"
        f"</div>"
        )

    return divisor.join(final)


  def traduzirAvaliacoes(self, avaliacoes):
    """
    Retorna uma string contendo o código HTML para as avaliações
    @avaliacoes: espera uma lista de dicionários contendo avaliações
    """
    if avaliacoes == "" or not len(avaliacoes): # Nenhuma avaliação no modelo especificado
      return "<h3 class='sem-avaliacoes padding-5'>Sem avaliações.</h3>"
    
    final = []

    # Cabeçalhos para avaliações, uma vez que sabe-se que há pelo menos uma
    final.append(
      f"<div class='avaliacao avaliacao-cabecalho'>"
        f"<h3 class='no-margin-heading padding-5 avaliacao-titulo'>Avaliações</h3>"
      f"</div>"
    )

    final.append(
      f"<div class='avaliacao avaliacao-titulos'>"
        f"<div class='avaliacao-item'>Nota</div>"
        f"<div class='avaliacao-item avaliacao-descricao'>Avaliação</div>"
        f"<div class='avaliacao-item'>Autor</div>"
      f"</div>"
    )

    aux = []
    divisor = "<hr class='divisor-horizontal'>"

    for avaliacao in avaliacoes:
      # Notação do Python para strings em múltiplas linhas.
      # Utilizada para se manter a hierarquia do HTML
      aux.append(
        f"<div class='avaliacao'>"
          f"<div class='avaliacao-item centro-vertical'>{round(avaliacao['nota'], 2)}</div>"
          f"<div class='avaliacao-item avaliacao-descricao'>{avaliacao['descricao']}</div>"
          f"<div class='avaliacao-item centro-vertical'>{avaliacao['autor']}</div>"
        f"</div>"
      )

    return ''.join(final) + divisor.join(aux)


  
  def traduzirPagamentos(self, pagamentos):
    """
    Retorna uma string contendo o código HTML para os pagamentos
    @avaliacoes: espera uma lista de dicionários contendo pagamentos
      Para este caso, pode haver de 0 a 2 elementos na lista, sendo no máximo um pagamento "à vista"
      e no máximo um pagamento "parcelado"
    """

    if pagamentos == "" or not len(pagamentos):
      return self.traduzirAVista({ 'modo': 'a vista', 'desconto': 0 })

    final = []
    for pagamento in pagamentos:
      if pagamento['modo'] == 'a vista':
        final.append(self.traduzirAVista(pagamento))
      else:
        final.append(self.traduzirParcelado(pagamento))

    return ''.join(final)


  def traduzirAVista(self, pagamento):
    """
    Retorna uma string contendo o código HTML para o pagamento à vista
    @avaliacoes: espera um dicionário contendo dados para o modo de pagamento
    """
    valor = self.variaveis['preco'] if pagamento['desconto'] == 0 else (
      (1 - pagamento['desconto']/100) * self.variaveis['preco']
    )

    desconto_string = "" if pagamento['desconto']== 0 else (f" - ({pagamento['desconto']}% de desconto)")

    return (
      f"<div class='padding-5'>"
        f"À vista: <b>R${round(valor, 2):.2f}</b>{desconto_string}"
      f"</div>"
    )


  def traduzirParcelado(self, pagamento):
    """
    Retorna uma string contendo o código HTML para o pagamento parcelado
    @avaliacoes: espera um dicionário contendo dados para o modo de pagamento
    """
    minimo, maximo = pagamento['de'], pagamento['ate']
    final = []

    final.append("<div class='padding-5'> Parcelado: <div id='parcelas'>")

    for i in range(minimo, maximo+1):
      valor = round(self.variaveis['preco']/i, 2)
      final.append(
        f"<div class='parcelado-item'>"
          f"{i}x de <b>R${valor}</b>"
        f"</div>"
      )
    
    final.append("</div></div>")

    return ''.join(final)


    