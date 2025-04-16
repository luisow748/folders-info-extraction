from typing import List

from model.TermoArbitramentoWrapper import TermoArbitramentoWrapper
from model.Imovel import Imovel

class ProcessosWrapper:
    """
    Classe que representa as informações de um processo.
    """
    def __init__(self, ano: str, numero: str, data: str, texto: str = "", termos_arbitramento: List[TermoArbitramentoWrapper] = [], imoveis: List[Imovel] = []):
        """
        :param ano: Ano a que o processo se refere (ex: '2025').
        :param numero: Número do processo (ex: '1234').
        :param data: Data composta por ano + mês + dia (ex: '20250305').
        :param texto: Conteúdo do texto extraído dos arquivos PDF do processo.
        """
        self.ano = ano
        self.numero = numero
        self.data = data
        self.texto = texto
        self.termos_arbitramento = termos_arbitramento
        self.imoveis = imoveis

    def __repr__(self):
        return f"ProcessosWrapper(ano={self.ano}, 
    numero={self.numero}, 
    data={self.data}, 
    texto_len={len(self.texto)}, 
    termos_arbitramento_len={len(self.termos_arbitramento)}, 
    imoveis_len={len(self.imoveis)})"