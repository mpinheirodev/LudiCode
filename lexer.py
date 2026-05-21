from sly import Lexer

class LudiCodeLexer(Lexer):
  tokens = { VAR, SE, SENAO, ENQUANTO, REPITA, FUNCAO, MOSTRAR, VERDADEIRO, FALSO, RETORNE, ID, NUMERO, TEXTO, IGUAL, ATRIBUICAO, MENOR, MAIOR, MENOR_IGUAL, MAIOR_IGUAL}

  ignore = ' \t'

  # Literais
  literals = { '=', '+', '-', '*', '/', '(', ')', '{', '}', ',', '.' }

  # Operadores relacionais
  IGUAL = r'=='
  MENOR_IGUAL = r'<='
  MAIOR_IGUAL = r'>='
  ATRIBUICAO = r'='
  MENOR = r'<'
  MAIOR = r'>'

  # Identificadores e palavras reservadas
  ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
  ID['var'] = VAR
  ID['se'] = SE
  ID['senão'] = SENAO 
  ID['enquanto'] = ENQUANTO
  ID['repita'] = REPITA
  ID['funcao'] = FUNCAO
  ID['mostrar'] = MOSTRAR
  ID['verdadeiro'] = VERDADEIRO
  ID['falso'] = FALSO
  ID['retorne'] = RETORNE

  # Números (inteiros e decimais)
  @_(r'\d+\.\d+|\d+')
    def NUMERO(self, t):
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

  # Textos (entre aspas)
  @_(r'".*?"')
    def TEXTO(self, t):
        t.value = t.value[1:-1] # Remove as aspas da string capturada
        return t

  # Comentários
  ignore_comment = r'//.*|#.*'

  # Quebra de linha
  @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)