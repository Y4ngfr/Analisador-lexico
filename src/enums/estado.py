import enum

class Estado(enum.Enum):
    INICIAL = 0
    TAG = 1
    IDENTIFICADOR = 2
    NUMERO = 3
    NUMERO_REAL = 4
    STRING_DUPLA = 5
    STRING_SIMPLES = 6
    VARIAVEL = 7
    OPERADOR = 8
    COMENTARIO_LINHA = 9
    MAIOR = 10
    MENOR = 11
    IGUAL = 12
    EXCLAMACAO = 13
    AND = 14
    OR = 15
    MAIS = 16
    MENOS = 17
    BARRA = 18
    PONTO = 19
    FINAL = 20