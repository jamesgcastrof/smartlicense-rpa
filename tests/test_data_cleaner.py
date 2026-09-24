import pandas as pd
from src.data_cleaner import clean_user_data


def test_clean_user_data_titles_and_accents():
    df = pd.DataFrame({
        "nome": ["Sr. Yuri da Conceição", "Ísis Borges"],
        "email": ["sr..yuri.da.conceicao@smartcorp.com.br", "isis.borges@smartcorp.com.br"]
    })
    res = clean_user_data(df)
    assert res.loc[0, "nome"] == "Yuri da Conceição"
    assert res.loc[1, "nome"] == "Ísis Borges"
    assert res.loc[0, "email"] == "yuri.da.conceicao@smartcorp.com.br"
    assert res.loc[1, "email"] == "isis.borges@smartcorp.com.br"
