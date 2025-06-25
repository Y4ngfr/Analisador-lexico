import os
import sys

from src.classes.analisador import AFDLexico
from src.classes.analisador import le_token

if __name__ == "__main__":
    nome_arquivo = sys.argv[1] if len(sys.argv) > 1 else "./codigo_teste/exemplo.php"
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