import re


def should_extract_pdf(pdf_name: str, pdf_extract_regex: str) -> bool:
    """
    Verifica se o nome do PDF corresponde ao padrão de regex para extração.

    :param pdf_name: Nome do arquivo PDF (ex: 'documento1.pdf').
    :param pdf_extract_regex: Regex definindo se o PDF deve ser extraído.
    :return: True se deve extrair o PDF, False caso contrário.
    """
    pattern = re.compile(pdf_extract_regex, re.IGNORECASE)
    return bool(pattern.match(pdf_name))