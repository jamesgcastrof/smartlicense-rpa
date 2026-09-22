import pandas as pd


def read_data_users(file_path):
    """
    Reads the raw users CSV file exported from the Admin Center.

    Args:
        file_path (str): Path to the CSV file to be read.
    
    Returns"
        pandas.DataFrame: Raw user data, whitout any cleaning applied.
    """
    df = pd.read_csv(file_path)
    return df

if __name__ == "__main__":
    df = read_data_users("../data/raw/usuarios_admin_center.csv")
    print(df.head())