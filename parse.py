from sly import Parser
from lexer import LudiCodeLexer


class LudiCodeParser(Parser):
    tokens = LudiCodeLexer.tokens

    precedence = (
        ('nonassoc', 'IGUAL', 'MENOR', 'MAIOR', 'MENOR_IGUAL', 'MAIOR_IGUAL'),
        ('left', '+', '-'),
        ('left', '*', '/'),
    )

    @_('statement')
    def program(self, p):
        return [p.statement]

    @_('program statement')
    def program(self, p):
        return p.program + [p.statement]

    @_('"{" program "}"')
    def bloco(self, p):
        return p.program

    @_('"{" statement "}"')
    def bloco(self, p):
        return [p.statement]

    @_('VAR ID ATRIBUICAO expr')
    def statement(self, p):
        return ('declaracao_var', p.ID, p.expr)

    @_('ID ATRIBUICAO expr')
    def statement(self, p):
        return ('atribuicao', p.ID, p.expr)

    @_('MOSTRAR "(" expr ")"')
    def statement(self, p):
        return ('mostrar', p.expr)

    @_('SE "(" expr ")" bloco')
    def statement(self, p):
        return ('se', p.expr, p.bloco)

    @_('SE "(" expr ")" bloco SENAO bloco')
    def statement(self, p):
        return ('se', p.expr, p.bloco0, p.bloco1)

    @_('SE "(" expr ")" bloco SENAO statement')
    def statement(self, p):
        return ('se', p.expr, p.bloco, [p.statement])

    @_('SE "(" expr ")" statement SENAO bloco')
    def statement(self, p):
        return ('se', p.expr, [p.statement], p.bloco)

    @_('ENQUANTO "(" expr ")" bloco')
    def statement(self, p):
        return ('enquanto', p.expr, p.bloco)

    @_('REPITA NUMERO bloco')
    def statement(self, p):
        return ('repita', p.NUMERO, p.bloco)

    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr',
       'expr IGUAL expr',
       'expr MENOR expr',
       'expr MAIOR expr',
       'expr MENOR_IGUAL expr',
       'expr MAIOR_IGUAL expr')
    def expr(self, p):
        return ('operacao', p[1], p.expr0, p.expr1)

    @_('NUMERO')
    def expr(self, p):
        return ('numero', p.NUMERO)

    @_('TEXTO')
    def expr(self, p):
        return ('texto', p.TEXTO)

    @_('VERDADEIRO')
    def expr(self, p):
        return ('booleano', True)

    @_('FALSO')
    def expr(self, p):
        return ('booleano', False)

    @_('ID')
    def expr(self, p):
        return ('variavel', p.ID)

    def error(self, p):
        if p:
            print(f"Erro de sintaxe na linha {p.lineno}: token inesperado '{p.value}'")
        else:
            print("Erro de sintaxe: fim de arquivo inesperado")
