import re
import pandas as pd
from unidecode import unidecode

def clean_user_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove títulos, normaliza espaços e reconstrói o e‑mail dos usuários.

    Parâmetros
    ----------
    df : pandas.DataFrame
        DataFrame contendo as colunas 'nome' e 'email'.

    Retorna
    -------
    pandas.DataFrame
        DataFrame com os nomes limpos e e‑mails reconstruídos.
    """
    # 1️ remover títulos e normalizar espaços
    title_regex = r'\b(?:sr\.?|sra\.?|dr\.?|dra\.? )\b\.?\s*'
    df['nome'] = df['nome'].str.replace(title_regex, '', flags=re.IGNORECASE, regex=True)
    df['nome'] = df['nome'].str.strip().str.replace(r'\s+', ' ', regex=True)

    # 2️ remover acentos para construir o e‑mail
    nome_sem_acento = df['nome'].apply(unidecode)

    # 3️ reconstruir e‑mail a partir do nome limpo
    dominio = df['email'].str.split('@').str[-1]                # mantém o domínio original
    df['email'] = nome_sem_acento.str.lower().str.replace(' ', '.') + '@' + dominio

    return df