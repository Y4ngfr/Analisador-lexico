import os
import sys

from classes.analisador import AFDLexico
from classes.analisador import le_token

if __name__ == "__main__":
    nome_arquivo = sys.argv[1]
    try:
        codigo = ''
        with open(nome_arquivo, 'r') as file:
            codigo = file.read()

        analisador = AFDLexico(codigo)
        analisador.analisar()

        if analisador.processador_estado.erros:
            print("\nErros encontrados:")
            for erro in analisador.processador_estado.erros:
                print(erro)

        print("\nTokens encontrados:")
        token = le_token(analisador)
        while token:
            print(token)
            token = le_token(analisador)

    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")