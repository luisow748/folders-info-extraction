class MatriculaWrapper:
    """
    Classe que representa as informações de uma matrícula.
    """
    def __init__(self, ano: str, numero: str, data: str, texto: str = ""):
        self.ano = ano
        self.numero = numero
        self.data = data
        self.texto = texto

    def __repr__(self):
        return f"MatriculaWrapper(ano={self.ano}, numero={self.numero}, data={self.data})"

