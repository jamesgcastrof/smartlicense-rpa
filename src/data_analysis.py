import numpy as np
import pandas as pd
from datetime import datetime


def process_user_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa os dados de usuários, calculando dias desde o último login, status e economia anual.

    Parâmetros
    ----------
    df : pandas.DataFrame
        DataFrame já limpo, contendo as colunas 'data_ultimo_login' e 'custo_mensal_licenca'.

    Retorna
    -------
    pandas.DataFrame
        DataFrame original com colunas adicionais:
        - dias_ultimo_login
        - status (ativo, alerta, inativo)
        - economia_anual_inativo
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