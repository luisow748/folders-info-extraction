import os
import re
from typing import List

from extraction.pdf.PDFExtractorStrategy import PDFExtractorStrategy
from extraction.pdf.impl.LocalPDFExtractorStrategy import LocalPDFExtractorStrategy
from model.ProcessosWrapper import ProcessosWrapper

"""
Exemplo completo de script Python que itera pastas de 'ano', 'mes' e 'processo',
cria um wrapper com informações do processo e extrai texto de PDFs via estratégia 
(local ou REST).
"""


def parse_process_folder_name(folder_name: str) -> (str, str):
    """
    Dado o nome de uma pasta de processo no formato:
      'XXX-XX-XXXX' ou 'XXX- XX- XXXX'
    Retorna uma tupla (dia, numeroProcesso), por exemplo ('05', '1234').

    :param folder_name: Nome da pasta do processo (ex: '01-05-1234').
    :return: Tupla (dia, numero).
    """
    # Normaliza possíveis espaços em excesso
    # Exemplo: '01- 05- 1234' => '01-05-1234'
    normalized = re.sub(r"\s*-\s*", "-", folder_name)
    # Agora esperamos um padrão 'XXX-XX-XXXX'
    parts = normalized.split('-')
    if len(parts) != 3:
        raise ValueError(f"Nome de pasta de processo inválido: {folder_name}")
    # parts[0] = XXX, parts[1] = XX (dia), parts[2] = XXXX (número processo)
    day = parts[1]
    process_number = parts[2]
    return day, process_number


def should_extract_pdf(pdf_name: str, pdf_extract_regex: str) -> bool:
    """
    Verifica se o nome do PDF corresponde ao padrão de regex para extração.

    :param pdf_name: Nome do arquivo PDF (ex: 'documento1.pdf').
    :param pdf_extract_regex: Regex definindo se o PDF deve ser extraído.
    :return: True se deve extrair o PDF, False caso contrário.
    """
    pattern = re.compile(pdf_extract_regex, re.IGNORECASE)
    return bool(pattern.match(pdf_name))


def process_directory(base_path: str,
                      extractor_strategy: PDFExtractorStrategy,
                      pdf_extract_regex: str = r".*\.pdf$") -> List[ProcessosWrapper]:
    """
    Itera pelas pastas de 'ano', 'mes' e 'processos' em um diretório base,
    cria objetos ProcessosWrapper e extrai texto (conforme estratégia definida)
    para cada PDF cujo nome bate com a regex informada.

    :param base_path: Caminho absoluto para a pasta base onde estão as pastas de ano.
    :param extractor_strategy: Estratégia de extração de PDF a ser utilizada.
    :param pdf_extract_regex: Regex que define quais PDFs devem ter seu texto extraído.
    :return: Lista de objetos ProcessosWrapper com dados e texto extraído.
    """

    all_wrappers = []

    # Iterar sobre as pastas de ano
    # Cada pasta deve ter um nome que represente o ano, ex.: "2024", "2025"
    if not os.path.isdir(base_path):
        raise NotADirectoryError(f"O caminho base fornecido não é um diretório válido: {base_path}")

    for ano in os.listdir(base_path):
        ano_path = os.path.join(base_path, ano)
        if not os.path.isdir(ano_path):
            continue  # Ignorar arquivos ou entradas que não sejam diretórios

        # Verifica se a pasta 'ano' realmente é um número
        if not ano.isdigit():
            # Caso não seja só número, pula
            continue

        # Iterar sobre as pastas de mês, ex.: "01", "02", "03", etc.
        for mes in os.listdir(ano_path):
            mes_path = os.path.join(ano_path, mes)
            if not os.path.isdir(mes_path):
                continue

            # Verifica se o 'mes' realmente é número
            if not mes.isdigit():
                continue

            # Iterar sobre as pastas de processos
            for process_folder in os.listdir(mes_path):
                process_path = os.path.join(mes_path, process_folder)
                if not os.path.isdir(process_path):
                    continue

                # Tenta extrair dia e numero do processo a partir do nome da pasta
                try:
                    dia, numero_processo = parse_process_folder_name(process_folder)
                except ValueError:
                    # Se não for um nome válido de pasta de processo, pular
                    continue

                # Monta a data = ano + mes + dia
                data_str = f"{ano}{mes}{dia}"

                # Cria o wrapper
                wrapper = ProcessosWrapper(
                    ano=ano,
                    numero=numero_processo,
                    data=data_str,
                    texto=""
                )

                # Itera pelos arquivos dentro desta pasta de processo
                for file_name in os.listdir(process_path):
                    file_path = os.path.join(process_path, file_name)

                    # Verifica se é PDF
                    if file_name.lower().endswith(".pdf"):
                        # Verifica se deve extrair texto deste PDF via regex
                        if should_extract_pdf(file_name, pdf_extract_regex):
                            # Extrai texto e concatena ao texto já existente
                            extracted = extractor_strategy.extract_text(file_path)
                            wrapper.texto += f"\n\n[Arquivo: {file_name}]\n{extracted}"

                    # Exemplo: caso queira tratar .docx futuramente, inclua aqui
                    # elif file_name.lower().endswith(".docx"):
                    #     pass  # lógica de extração de .docx

                # Adiciona esse wrapper à lista final
                all_wrappers.append(wrapper)

    return all_wrappers


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
