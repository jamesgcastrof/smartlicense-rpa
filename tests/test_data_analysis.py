import pytest
import pandas as pd
from datetime import datetime, timedelta
from src.data_analysis import process_user_data


@pytest.mark.parametrize("days_ago,expected_status", [
    (30, "ativo"),
    (31, "alerta"),
    (90, "alerta"),
    (91, "inativo")
])
def test_process_user_data_thresholds(days_ago, expected_status):
    ref_date = datetime(2026, 9, 22)
    login_date = (ref_date - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    df = pd.DataFrame({
        "data_ultimo_login": [login_date],
        "custo_mensal_licenca": [35.0]
    })
    res = process_user_data(df)
    assert res.loc[0, "status"] == expected_status
    if expected_status != "inativo":
        assert res.loc[0, "economia_anual_inativo"] == 0.0
    else:
        assert res.loc[0, "economia_anual_inativo"] == 420.0
