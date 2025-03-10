from typing import List
import os

from extraction.pdf.PDFExtractorStrategy import PDFExtractorStrategy
from model.ProcessosWrapper import ProcessosWrapper
from service.parse_process_folder_name import parse_process_folder_name
from service.should_extract_pdf import should_extract_pdf



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