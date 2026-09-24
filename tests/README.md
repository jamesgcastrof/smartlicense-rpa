# Testes automatizados

- **conftest.py** – Configurações globais de fixtures; adiciona o diretório raiz ao `sys.path` para permitir importação de módulos `src`.
- **test_data_cleaner.py** – Verifica a remoção de títulos e a normalização de nomes e e‑mails (casos U0048 e U0003).
- **test_data_analysis.py** – Valida a classificação de status (ativo/alerta/inativo) nos limites de 30, 31, 90 e 91 dias e o cálculo da economia anual para usuários inativos.
- **test_email_notifier.py** – Testa o envio bem‑sucedido de e‑mail com anexo usando `unittest.mock` e garante que um `ConnectionRefusedError` resulta em `RuntimeError`.
- **test_pipeline_integration.py** – Executa o pipeline completo (leitura, limpeza, análise) sobre o CSV real e verifica que o usuário **U0048** aparece como “inativo” com economia `420.0`.
- **test_report_writer.py** – Confirma que `export_report` cria um arquivo Excel contendo as abas “Resumo” e “Detalhes”.
