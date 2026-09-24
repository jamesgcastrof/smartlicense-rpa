from src.data_reader import read_data_users
from src.data_cleaner import clean_user_data
from src.data_analysis import process_user_data
from src.report_writer import export_report


import schedule, time
from datetime import datetime

def iniciar_agendamento():
    # intervalo de demonstração (2 minutos). Em produção: schedule.every().day.at("08:00").do(run)
    schedule.every(2).minutes.do(run)
    while True:
        schedule.run_pending()
        time.sleep(5)


def run():
    raw = read_data_users('data/raw/usuarios_admin_center.csv')
    clean = clean_user_data(raw)
    final = process_user_data(clean)

    output_path = 'data/processed/relatorio_smartlicense.xlsx'
    export_report(final, output_path)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Pipeline executado com sucesso.")


if __name__ == '__main__':
    # run()  # Executa apenas uma vez (descomente para uso sem agendamento)
    iniciar_agendamento()  # Executa com agendamento (demo)