import numpy as np
import pandas as pd
from datetime import datetime


def process_user_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    1 Define a data de referência fixa (22/09/2026)
    2 Calcula a quantidade de dias desde o último login
    3 Cria a coluna "status": ativo (<=30), alerta (31-90), inativo (>90)
    4 Calcula a economia anual projetada por usuário inativo (custo_mensal * 12)
    5 Insere "economia_anual_inativo" no DataFrame (0 para não inativos)

    Args:
        df (pd.DataFrame): DataFrame já limpo (ver data_cleaner.py),
            contendo as colunas 'data_ultimo_login' e 'custo_mensal_licenca'.

    Returns:
        pd.DataFrame: DataFrame original com as colunas adicionais
            'dias_ultimo_login', 'status' e 'economia_anual_inativo'.
    """
    ref_date = datetime(2026, 9, 22)
    df["data_ultimo_login"] = pd.to_datetime(df["data_ultimo_login"], errors="coerce")
    df["dias_ultimo_login"] = (ref_date - df["data_ultimo_login"]).dt.days

    conditions = [
        df["dias_ultimo_login"] <= 30,
        df["dias_ultimo_login"].between(31, 90),
        df["dias_ultimo_login"] > 90,
    ]
    choices = ["ativo", "alerta", "inativo"]
    df["status"] = np.select(conditions, choices, default="indefinido")

    df["economia_anual_inativo"] = 0.0
    inativos = df["status"] == "inativo"
    df.loc[inativos, "economia_anual_inativo"] = df.loc[inativos, "custo_mensal_licenca"] * 12

    return df