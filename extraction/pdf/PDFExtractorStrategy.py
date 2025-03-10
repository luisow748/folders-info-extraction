from typing import Protocol


class PDFExtractorStrategy(Protocol):
    """
    Define o protocolo (interface) que toda estratégia de extração de PDF deve seguir.
    """
    def extract_text(self, pdf_path: str) -> str:
        """
        Extrai o texto de um arquivo PDF a partir do caminho informado.

        :param pdf_path: Caminho absoluto para o PDF.
        :return: Texto extraído do PDF.
        """
        ...