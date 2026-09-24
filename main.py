from src.data_reader import read_data_users
from src.data_cleaner import clean_user_data
from src.data_analysis import process_user_data
from src.report_writer import export_report


def run():
    raw = read_data_users('data/raw/usuarios_admin_center.csv')
    clean = clean_user_data(raw)
    final = process_user_data(clean)

    output_path = 'data/processed/relatorio_smartlicense.xlsx'
    export_report(final, output_path)

    print(f"Relatório gerado com sucesso em: {output_path}")


if __name__ == '__main__':
    run()