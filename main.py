from src.data_reader import read_data_users
from src.data_cleaner import clean_user_data
from src.data_analysis import process_user_data
from src.report_writer import export_report


import logging
import os
import schedule, time
from pathlib import Path
from datetime import datetime


def configurar_logging():
    """Configura logger com FileHandler (arquivo timestamp) e StreamHandler."""
    log_dir = Path('logs/execution')
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'execucao_{timestamp}.log'
    logger = logging.getLogger('pipeline')
    # Remove any existing handlers to avoid duplicate logs on successive runs
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # File handler
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def iniciar_agendamento():
    # intervalo de demonstração (2 minutos). Em produção: schedule.every().day.at("08:00").do(run)
    schedule.every(2).minutes.do(run)
    while True:
        schedule.run_pending()
        time.sleep(5)


def run():
    # Configura logging para esta execução
    logger = configurar_logging()
    try:
        logger.info("Iniciando execução do pipeline SmartLicense RPA.")
        raw = read_data_users('data/raw/usuarios_admin_center.csv')
        logger.info(f"{len(raw)} usuários lidos do arquivo CSV.")
        clean = clean_user_data(raw)
        final = process_user_data(clean)

        # Resumo de status e economia
        status_counts = final["status"].value_counts()
        contagem_ativo = status_counts.get("ativo", 0)
        contagem_alerta = status_counts.get("alerta", 0)
        contagem_inativo = status_counts.get("inativo", 0)
        economia_total = final["economia_anual_inativo"].sum()
        logger.info(f"Status: {contagem_ativo} ativos, {contagem_alerta} em alerta, {contagem_inativo} inativos.")
        logger.info(f"Economia anual potencial: R$ {economia_total:.2f}")

        output_path = 'data/processed/relatorio_smartlicense.xlsx'
        export_report(final, output_path)
        logger.info(f"Relatório gerado com sucesso em: {output_path}")
    except Exception as exc:
        logger.error(f"Erro durante a execução do pipeline: {exc}", exc_info=True)
        raise



if __name__ == '__main__':
    # run()  # Executa apenas uma vez (descomente para uso sem agendamento)
    iniciar_agendamento()  # Executa com agendamento (demo)