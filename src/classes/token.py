class Token:
    def __init__(self, tipo, valor, linha):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha

    def __str__(self):
        return f"Token(tipo='{self.tipo}', valor='{self.valor}', linha='{self.linha}')"
