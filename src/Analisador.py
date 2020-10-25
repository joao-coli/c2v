class Analisador:

  def mostrarErro(self, mensagem, linha):
     print(f"Erro na linha {linha}: {mensagem}")


class AnalisadorSemantico(Analisador):

  def mostrarErroJaDeclarado(self, atributo, linha):
    self.mostrarErro(f"'{atributo}' já definido anteriormente", linha)

  # Erro sintático de atributo obrigatório não declarado
  def mostrarErroNaoDeclarado(self, atributo):
    print(f"Erro: Atributo obrigatório '{atributo}' não declarado")