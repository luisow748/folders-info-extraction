import re


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