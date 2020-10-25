from textx.exceptions import TextXSyntaxError, TextXSemanticError
from .Analisador import Analisador

class C2VSintatico(Analisador):

  def __init__(self, meta_modelo):
    self.meta_modelo = meta_modelo


  def analisar(self, arquivo):
    try:
      modelo = self.meta_modelo.model_from_file(arquivo) # Cria o modelo a partir do meta modelo
    except TextXSyntaxError as e: # Erro léxico/ sintático
      parser = e.__context__.parser # Instância do parser do textX
      parser.position = e.__context__.position # Posição da ocorrência do erro
      self.mostrarErro(f"sequencia nao reconhecida proximo a '{parser.context()}'", e.line)
      return False

    return modelo