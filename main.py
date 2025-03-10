from extraction.pdf.impl.LocalPDFExtractorStrategy import LocalPDFExtractorStrategy
from service.process_directory import process_directory


def main():
    """
    Função principal de exemplo que mostra como usar o script.

    1. Define o caminho base (onde estão as pastas de ano).
    2. Escolhe a estratégia de extração de PDF.
    3. Define a regex para filtrar quais PDFs devem ser extraídos.
    4. Executa o processamento e imprime o resultado.
    """

    # Exemplo de caminho base (ajuste conforme sua estrutura)
    base_path = r"C:\Caminho\para\pasta\anos"  # Ajuste para o seu caso real

    # Escolha qual estratégia de extração deseja utilizar:
    # 1) Extração local usando PyPDF2
    extractor = LocalPDFExtractorStrategy()

    # 2) OU: Extração via REST
    # extractor = RestPDFExtractorStrategy(api_url="http://exemplo-minha-api/extrair-texto")

    # Exemplos de regex:
    # - Para extrair todos PDFs: r".*\.pdf$"
    # - Para extrair apenas PDFs cujo nome inicia com 'IMP': r"IMP.*\.pdf$"
    pdf_extract_regex = r".*\.pdf$"

    # Processa diretório e obtém lista de ProcessosWrapper
    wrappers = process_directory(base_path, extractor, pdf_extract_regex)

    # Exibe o resultado
    for w in wrappers:
        print(w)
        # Se quiser imprimir o texto extraído na íntegra:
        # print(w.texto)


if __name__ == "__main__":
    main()
