import pytest
import pandas as pd
from src.data_reader import read_data_users
from src.data_cleaner import clean_user_data
from src.data_analysis import process_user_data
from src.report_writer import export_report


def test_full_pipeline(tmp_path):
    # usa o CSV real
    df_raw = read_data_users("data/raw/usuarios_admin_center.csv")
    df_clean = clean_user_data(df_raw)
    df_final = process_user_data(df_clean)
    # verifica usuário U0048
    u = df_final[df_final["usuario_id"] == "U0048"].iloc[0]
    assert u["status"] == "inativo"
    assert u["economia_anual_inativo"] == 420.0
    # gera relatório temporário
    out_file = tmp_path / "relatorio.xlsx"
    export_report(df_final, str(out_file))
    assert out_file.exists()
