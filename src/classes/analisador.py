import sys
from enums.estado import Estado
from classes.processador_estado import ProcessadorEstado

class AFDLexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.processador_estado = ProcessadorEstado(Estado.INICIAL, self.codigo)

    def analisar(self):
        while self.processador_estado.get_posicao() < len(self.codigo):
            char = self.codigo[self.processador_estado.get_posicao()]

            self.processador_estado.processar_estado(char)

            # Avança para o próximo caractere
            self.processador_estado.avancar_posicao()
            
            # Trata quebras de linha para contagem
            if char == '\n':
                self.processador_estado.avancar_linha()
        
        # Processa qualquer lexema pendente no final do arquivo
        self.processador_estado.finalizar_lexema()


def le_token(analisador):
    if not hasattr(analisador.processador_estado, 'token_index'):
        analisador.processador_estado.token_index = 0

    if analisador.processador_estado.token_index < len(analisador.processador_estado.tokens):
        token = analisador.processador_estado.tokens[analisador.processador_estado.token_index]
        analisador.processador_estado.token_index += 1
        return token

    return None

