import re
import pandas as pd

def clean_user_data(df: pd.DataFrame) -> pd.DataFrame:
    # 1 remover títulos do nome
    title_pattern = r'\b(?:Sr\.?|Sra\.?|Dra\.?|Dr\.?)\b\.?\s*'
    df['nome'] = df['nome'].str.replace(title_pattern, '', flags=re.IGNORECASE, regex=True)

    # 2️ corrigir e‑mails com pontos duplos ou ponto antes de '@'
    df['email'] = (
        df['email']
        .str.replace(r'\.{2,}', '.', regex=True)          # ".." → "."
        .str.replace(r'\.@', '@', regex=True)            # ".@" → "@"
    )

    return df