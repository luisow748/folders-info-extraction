from model.MatriculaWrapper import MatriculaWrapper


class Imovel:
    """
    Classe que representa as informações de um imóvel.
    """
    def __init__(self, inscricao_imobiliaria: str, matricula: MatriculaWrapper, descricao: str = ""):
        self.inscricao_imobiliaria = inscricao_imobiliaria
        self.matricula = matricula
        self.descricao = descricao

    def __repr__(self):
        return f"Imovel(inscricao_imobiliaria={self.inscricao_imobiliaria}, matricula_numero={self.matricula.numero}, descricao={self.descricao})"

