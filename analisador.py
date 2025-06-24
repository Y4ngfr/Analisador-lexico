import re
import sys

class Token:
    def __init__(self, tipo, valor, linha):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha

    def __str__(self):
        return f"Token(tipo='{self.tipo}', valor='{self.valor}', linha='{self.linha}')"

class AnalisadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.posicao = 0
        self.linha_atual = 1
        self.tokens = []
        self.erros = []

        self.regras = [
            # Tags PHP (devem vir primeiro)
            (r'<\?php|<\?', 'TAG_ABERTURA'),
            (r'\?>', 'TAG_FECHAMENTO'),

            # Funções específicas (antes das palavras-chave)
            (r'echo\("([^"]*)"\)', 'ECHO'),
            (r'printf\("([^"]*)"\)', 'PRINTF'),
            (r'fgets\(STDIN\)', 'FGETS'),
            (r'readline\("([^"]*)"\)', 'READLINE'),

            # Operadores de comparação (antes dos operadores aritméticos)
            (r'===|!==|==|!=|<=|>=', 'OPERADOR_COMPARACAO'),
            (r'&&|\|\|', 'OPERADOR_LOGICO'),
            (r'\+\+|--', 'OPERADOR_INCREMENTO'),
            
            # Operadores aritméticos
            (r'[\+\-\*/%]', 'OPERADOR_ARITMETICO'),
            
            # Operadores e delimitadores
            (r'=', 'ATRIBUICAO'),
            (r'>', 'MAIOR'),
            (r'<', 'MENOR'),
            (r'[;,\(\)\{\}\[\]]', 'DELIMITADOR'),

            # Palavras-chave
            (r'\b(if|else|elseif|while|for|foreach|function|return|break|continue)\b', 'PALAVRA_CHAVE'),
            (r'\b(echo|print)\b', 'PALAVRA_CHAVE'),  # echo e print genéricos

            # Tipos e valores especiais
            (r'\b(true|false|null)\b', 'VALOR_ESPECIAL'),

            # Números
            (r'\d+\.\d+', 'NUMERO_REAL'),
            (r'\d+', 'NUMERO_INTEIRO'),

            # Strings (simplificado)
            (r'"(?:[^"\\]|\\.)*"', 'STRING_DUPLA'),
            (r"'(?:[^'\\]|\\.)*'", 'STRING_SIMPLES'),

            (r'\$[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*', 'VARIAVEL'),

            (r'[A-Z_][A-Z0-9_]*\b', 'CONSTANTE'),

            (r'[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*', 'IDENTIFICADOR'),

            # Espaços e comentários (ignorados)
            (r'\s+', None),
            (r'//.*', None),
            (r'#.*', None),

            (r'[\+\-\*/%]=', 'OPERADOR_ATRIBUICAO_COMBINADA'),

            (r'\.', 'OPERADOR_CONCATENACAO'),

        ]

        self.regras_regex = []
        for padrao, tag in self.regras:
            self.regras_regex.append((re.compile(padrao), tag))

    def analisar(self):
        while self.posicao < len(self.codigo):
            match = None
            for regex, tag in self.regras_regex:
                regex_match = regex.match(self.codigo, self.posicao)
                if regex_match:
                    match = regex_match
                    if tag:                         # Se não for None
                        valor = match.group(0)
                        token = Token(tag, valor, self.linha_atual)
                        self.tokens.append(token)
                    break

            if not match:
                erro = f"Caractere inesperado '{self.codigo[self.posicao]}' na linha {self.linha_atual}"
                self.erros.append(erro)
                self.posicao += 1

            else:
                if '\n' in match.group(0):
                    self.linha_atual += match.group(0).count('\n')
                self.posicao = match.end()

        return self.tokens, self.erros
    

def le_token(analisador):
    if not hasattr(analisador, 'token_index'):
        analisador.token_index = 0

    if analisador.token_index < len(analisador.tokens):
        token = analisador.tokens[analisador.token_index]
        analisador.token_index += 1
        return token
    else:
        return None
    
if __name__ == "__main__":
    nome_arquivo = sys.argv[1]
    try:
        with open(nome_arquivo, 'r') as file:
            codigo = file.read()

        analisador = AnalisadorLexico(codigo)
        token, erros = analisador.analisar()

        if erros:
            print("\nErros encontrados:")
            for erro in erros:
                print(erro)

        print("\nTokens encontrados:")
        token = le_token(analisador)
        while token:
            print(token)
            token = le_token(analisador)

    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
