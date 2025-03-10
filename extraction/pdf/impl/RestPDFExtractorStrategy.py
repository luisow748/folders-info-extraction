import os
import requests

from extraction.pdf.PDFExtractorStrategy import PDFExtractorStrategy


class RestPDFExtractorStrategy(PDFExtractorStrategy):
    """
    Estratégia concreta de extração de texto de PDF via requisição REST, 
    usando a biblioteca requests.
    Documentação: https://pypi.org/project/requests/
    """
    def __init__(self, api_url: str):
        """
        :param api_url: URL da API responsável por extrair o texto do PDF.
                        (Por exemplo: "http://minha-api.com/extrair-texto")
        """
        self.api_url = api_url

    def extract_text(self, pdf_path: str) -> str:
        """
        Exemplo de chamada a uma API que recebe um PDF e retorna o texto.
        Você pode adaptar conforme o formato de envio exigido pela sua API.
        """
        with open(pdf_path, 'rb') as file:
            # Exemplo de envio multipart/form-data
            files = {'file': (os.path.basename(pdf_path), file, 'application/pdf')}
            response = requests.post(self.api_url, files=files)

        if response.status_code == 200:
            return response.text
        else:
            # Trate possíveis erros de forma adequada
            return ""