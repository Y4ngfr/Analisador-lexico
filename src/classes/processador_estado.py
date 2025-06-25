from enums.estado import Estado
from classes.token import Token

class ProcessadorEstado:
    def __init__(self, estado_inicial, codigo):
        self.estado_atual = estado_inicial
        self.codigo = codigo
        self.erros = []
        self.lexema = ""
        self.inicio_lexema = 0
        self.tokens = []
        self.posicao = 0
        self.linha_atual = 1

    def processar_estado(self, char):
        if self.estado_atual == Estado.INICIAL:
            self.processar_estado_inicial(char)
        elif self.estado_atual == Estado.TAG:
            self.processar_estado_tag(char)
        elif self.estado_atual == Estado.IDENTIFICADOR:
            self.processar_estado_identificador(char)
        elif self.estado_atual == Estado.NUMERO:
            self.processar_estado_numero(char)
        elif self.estado_atual == Estado.NUMERO_REAL:
            self.processar_estado_numero_real(char)
        elif self.estado_atual == Estado.STRING_DUPLA:
            self.processar_estado_string_dupla(char)
        elif self.estado_atual == Estado.STRING_SIMPLES:
            self.processar_estado_string_simples(char)
        elif self.estado_atual == Estado.VARIAVEL:
            self.processar_estado_variavel(char)
        elif self.estado_atual == Estado.COMENTARIO_LINHA:
            self.processar_estado_comentario_linha(char)
        elif self.estado_atual == Estado.MAIOR:
            self.processar_estado_maior(char)
        elif self.estado_atual == Estado.MENOR:
            self.processar_estado_menor(char)
        elif self.estado_atual == Estado.IGUAL:
            self.processar_estado_igual(char)
        elif self.estado_atual == Estado.EXCLAMACAO:
            self.processar_estado_exclamacao(char)
        elif self.estado_atual == Estado.AND:
            self.processar_estado_and(char)
        elif self.estado_atual == Estado.OR:
            self.processar_estado_or(char)
        elif self.estado_atual == Estado.MAIS:
            self.processar_estado_mais(char)
        elif self.estado_atual == Estado.MENOS:
            self.processar_estado_menos(char)
        elif self.estado_atual == Estado.BARRA:
            self.processar_estado_barra(char)

    def processar_estado_inicial(self, char):
        if char == '<':
            self.manipular_estado(Estado.MENOR, char)
        elif char == '>':
            self.manipular_estado(Estado.MAIOR, char)
        elif char == '?':
            self.manipular_estado(Estado.TAG, char)
        elif char == '=':
            self.manipular_estado(Estado.IGUAL, char)
        elif char == '!':
            self.manipular_estado(Estado.EXCLAMACAO, char)
        elif char == '&':
            self.manipular_estado(Estado.AND, char)
        elif char == '|':
            self.manipular_estado(Estado.OR, char)
        elif char == '+':
            self.manipular_estado(Estado.MAIS, char)
        elif char == '-':
            self.manipular_estado(Estado.MENOS, char)
        elif char == '/':
            self.manipular_estado(Estado.BARRA, char)
        elif char == '"':
            self.manipular_estado(Estado.STRING_DUPLA, char)
        elif char == "'":
            self.manipular_estado(Estado.STRING_SIMPLES, char)
        elif char == '$':
            self.manipular_estado(Estado.VARIAVEL, char)
        elif char.isalpha() or char == '_':
            self.manipular_estado(Estado.IDENTIFICADOR, char)
        elif char.isdigit():
            self.manipular_estado(Estado.NUMERO, char)
        elif char in [';', ',', '(', ')', '{', '}', '[', ']']:
            self.adicionar_token('DELIMITADOR', char)
        elif char in [' ', '\t', '\n', '\r']:
            # Espaços em branco são ignorados
            pass
        else:
            self.erros.append(f"Caractere inesperado '{char}' na linha {self.linha_atual}")

    def manipular_estado(self, estado_atual, lexama):
        self.estado_atual = estado_atual
        self.inicio_lexema = self.posicao
        self.lexema = lexama

    def processar_estado_tag(self, char):
        if char == '>':
            self.lexema += char
            self.adicionar_token('TAG_FECHAMENTO', self.lexema)
            self.manipular_estado(Estado.INICIAL, "")
        else:
            self.erros.append(f"Operador inesperado '{self.lexema}' na linha {self.linha_atual}")

    def processar_estado_identificador(self, char):
        if char.isalpha() or char.isdigit() or char == '_':
            self.lexema += char
            return

        palavras_chave = {
            'if': 'PALAVRA_CHAVE',
            'else': 'PALAVRA_CHAVE',
            'elseif': 'PALAVRA_CHAVE',
            'while': 'PALAVRA_CHAVE',
            'for': 'PALAVRA_CHAVE',
            'foreach': 'PALAVRA_CHAVE',
            'function': 'PALAVRA_CHAVE',
            'return': 'PALAVRA_CHAVE',
            'break': 'PALAVRA_CHAVE',
            'continue': 'PALAVRA_CHAVE',
            'echo': 'PALAVRA_CHAVE',
            'print': 'PALAVRA_CHAVE',
            'true': 'VALOR_ESPECIAL',
            'false': 'VALOR_ESPECIAL',
            'null': 'VALOR_ESPECIAL'
        }

        tipo = palavras_chave.get(self.lexema, 'IDENTIFICADOR')
        self.adicionar_token(tipo, self.lexema)
        self.retornar_posicao()
        self.manipular_estado(Estado.INICIAL, "")

    def processar_estado_numero(self, char):
        if char.isdigit():
            self.lexema += char
        elif char == '.':
            self.lexema += char
            self.manipular_estado(Estado.NUMERO_REAL, self.lexema)
        else:
            self.adicionar_token('NUMERO_INTEIRO', self.lexema)
            self.retornar_posicao()
            self.manipular_estado(Estado.INICIAL, "")

    def processar_estado_numero_real(self, char):
        if char.isdigit():
            self.lexema += char
            return

        self.retornar_posicao()
        self.adicionar_token('NUMERO_REAL', self.lexema)
        self.manipular_estado(Estado.INICIAL, "")

    def processar_estado_string_dupla(self, char):
        self.lexema += char
        if char == '"' and self.lexema[0] == '"' and len(self.lexema) > 1:
            self.adicionar_token('STRING_DUPLA', self.lexema)
            self.manipular_estado(Estado.INICIAL, "")

    def processar_estado_string_simples(self, char):
        self.lexema += char
        if char == "'" and self.lexema[0] == "'" and len(self.lexema) > 1:
            self.adicionar_token('STRING_SIMPLES', self.lexema)
            self.manipular_estado(Estado.INICIAL, "")

    def processar_estado_variavel(self, char):
        if char.isalpha() or char.isdigit() or char == '_':
            self.lexema += char
        else:
            self.adicionar_token('VARIAVEL', self.lexema)
            self.retornar_posicao()
            self.manipular_estado(Estado.INICIAL, "")

    def processar_estado_comentario_linha(self, char):
        if char == '\n':
            self.estado_atual = Estado.INICIAL

    def processar_estado_maior(self, char):
        if char == '=':
            self.lexema += char
            self.adicionar_token('OPERADOR_COMPARACAO', self.lexema)
        else:
            self.adicionar_token('MAIOR', self.lexema)
            self.retornar_posicao()
        self.manipular_estado(Estado.INICIAL, "")

    def processar_estado_menor(self, char):
        if char == '?':
            self.lexema += char
            if self.posicao + 3 < len(self.codigo) and self.codigo[self.posicao+1:self.posicao+4] == 'php':
                self.lexema += 'php'
                self.posicao += 3
                self.adicionar_token('TAG_ABERTURA', self.lexema)
            else:
                self.adicionar_token('TAG_ABERTURA', self.lexema)
        elif char == '=':
            self.lexema += char
            self.adicionar_token('OPERADOR_COMPARACAO', self.lexema)
        else:
            self.adicionar_token('MENOR', self.lexema)
            self.retornar_posicao()
        self.manipular_estado(Estado.INICIAL, "")

    def processar_estado_igual(self, char):
        if char == '=':
            self.lexema += char
            self.adicionar_token('OPERADOR_COMPARACAO', self.lexema)
        else:
            self.adicionar_token('ATRIBUICAO', self.lexema)
            self.retornar_posicao()
        self.manipular_estado(Estado.INICIAL, "")

    def processar_estado_exclamacao(self, char):
        if char == '=':
            self.lexema += char
            if self.posicao + 1 < len(self.codigo) and self.codigo[self.posicao + 1] == '=':
                self.lexema += '='
                self.adicionar_token('OPERADOR_COMPARACAO', self.lexema)
            else:
                self.adicionar_token('OPERADOR_COMPARACAO', self.lexema)
        else:
            self.erros.append(f"Operador inesperado '{self.lexema}' na linha {self.linha_atual}")
        self.manipular_estado(Estado.INICIAL, "")

    def processar_estado_and(self, char):
        if char == '&':
            self.lexema += char
            self.adicionar_token('OPERADOR_LOGICO', self.lexema)
        else:
            self.erros.append(f"Operador inesperado '{self.lexema}' na linha {self.linha_atual}")
        self.manipular_estado(Estado.INICIAL, "")

    def processar_estado_or(self, char):
        if char == '|':
            self.lexema += char
            self.adicionar_token('OPERADOR_LOGICO', self.lexema)
        else:
            self.erros.append(f"Operador inesperado '{self.lexema}' na linha {self.linha_atual}")
        self.manipular_estado(Estado.INICIAL, "")

    def processar_estado_mais(self, char):
        if char == '+':
            self.lexema += char
            self.adicionar_token('OPERADOR_INCREMENTO', self.lexema)
        elif char == '=':
            self.lexema += char
            self.adicionar_token('OPERADOR_ATRIBUICAO_COMBINADA', self.lexema)
        else:
            self.adicionar_token('OPERADOR_ARITMETICO', self.lexema)
            self.retornar_posicao()
        self.manipular_estado(Estado.INICIAL, "")

    def processar_estado_menos(self, char):
        if char == '-':
            self.lexema += char
            self.adicionar_token('OPERADOR_INCREMENTO', self.lexema)
        elif char == '=':
            self.lexema += char
            self.adicionar_token('OPERADOR_ATRIBUICAO_COMBINADA', self.lexema)
        else:
            self.adicionar_token('OPERADOR_ARITMETICO', self.lexema)
            self.retornar_posicao()
        self.manipular_estado(Estado.INICIAL, "")

    def processar_estado_barra(self, char):
        if char == '/':
            self.manipular_estado(Estado.COMENTARIO_LINHA, "")
        elif char == '=':
            self.lexema += char
            self.adicionar_token('OPERADOR_ATRIBUICAO_COMBINADA', self.lexema)
        else:
            self.adicionar_token('OPERADOR_ARITMETICO', self.lexema)
            self.retornar_posicao()
        self.manipular_estado(Estado.INICIAL, "")

    def finalizar_lexema(self):
        if self.lexema:
            if self.estado_atual == Estado.IDENTIFICADOR:
                self.processar_estado_identificador('')
            elif self.estado_atual == Estado.NUMERO:
                self.adicionar_token('NUMERO_INTEIRO', self.lexema)
            elif self.estado_atual == Estado.NUMERO_REAL:
                self.adicionar_token('NUMERO_REAL', self.lexema)
            elif self.estado_atual == Estado.STRING_DUPLA:
                self.erros.append(f"String não fechada '{self.lexema}' na linha {self.linha_atual}")
            elif self.estado_atual == Estado.STRING_SIMPLES:
                self.erros.append(f"String não fechada '{self.lexema}' na linha {self.linha_atual}")
            elif self.estado_atual == Estado.VARIAVEL:
                self.adicionar_token('VARIAVEL', self.lexema)
            else:
                self.erros.append(f"Sequência inesperada '{self.lexema}' na linha {self.linha_atual}")
            self.manipular_estado(Estado.INICIAL, "")

    def get_posicao(self):
        return self.posicao

    def avancar_posicao(self):
        self.posicao += 1

    def retornar_posicao(self):
        self.posicao -= 1

    def avancar_linha(self):
        self.linha_atual += 1

    def adicionar_token(self, tipo, valor):
        self.tokens.append(Token(tipo, valor, self.linha_atual))
        self.lexema = ""