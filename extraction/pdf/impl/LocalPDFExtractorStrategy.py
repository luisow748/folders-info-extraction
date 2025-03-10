from extraction.pdf.PDFExtractorStrategy import PDFExtractorStrategy


class LocalPDFExtractorStrategy(PDFExtractorStrategy):
    """
    Estratégia concreta de extração de texto de PDF localmente, 
    utilizando a biblioteca PyPDF2.
    Documentação: https://pypi.org/project/PyPDF2/
    """
    def extract_text(self, pdf_path: str) -> str:
        import PyPDF2
        extracted_text = []

        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted_text.append(page.extract_text() or "")

        return "\n".join(extracted_text)