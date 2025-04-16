from typing import List

from model.MatriculaWrapper import MatriculaWrapper
from model.ProcessosWrapper import ProcessosWrapper

class TermoArbitramentoWrapper:
    """
    Classe que representa as informações de um termo de arbitramento.
    """
    def __init__(self, processo: ProcessosWrapper, requerente: str, agente_emissor: str, objeto: str, data: str, matriculas: List[MatriculaWrapper] = []):
        self.processo = processo
        self.requerente = requerente
        self.agente_emissor = agente_emissor
        self.objeto = objeto
        self.data = data
        self.matriculas = matriculas

    def __repr__(self):
        return f"TermoArbitramentoWrapper(processo_ano={self.processo.ano}, 
    processo_numero={self.processo.numero}, 
    processo_data={self.processo.data}, 
    requerente={self.requerente}, 
    agente_emissor={self.agente_emissor},
    objeto={self.objeto}, 
    data={self.data})"

