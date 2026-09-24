import pandas as pd


def read_data_users(file_path):
    """
    Lê o CSV bruto de usuários exportado do Admin Center.

    Parâmetros
    ----------
    file_path : str
        Caminho para o arquivo CSV a ser lido.

    Retorna
    -------
    pandas.DataFrame
        Dados dos usuários sem limpeza.

    Raises
    ------
    FileNotFoundError
        Se o arquivo não for encontrado.
    """
    df = pd.read_csv(file_path)
    return df

if __name__ == "__main__":
    df = read_data_users("../data/raw/usuarios_admin_center.csv")
    print(df.head())