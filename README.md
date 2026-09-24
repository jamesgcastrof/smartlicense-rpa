# SmartLicense RPA

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.49-43B02A?logo=selenium&logoColor=white)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Sistema de RPA (Robotic Process Automation) que audita licenças e acessos
de usuários corporativos, identifica contas inativas, projeta a economia
financeira ao revogar essas licenças e gera um relatório executivo em
Excel — como parte de um projeto de portfólio em Engenharia de Dados.

> Projeto simulado: os dados de usuários são gerados artificialmente
> (não é uma integração real com nenhum Admin Center), especificamente
> para praticar limpeza de dados, ETL e automação de ponta a ponta.

---

## Por que esse projeto existe

Empresas frequentemente pagam por licenças de software (Office 365,
Salesforce, VPN, etc.) atribuídas a colaboradores que pararam de usá‑las
há meses — contas inativas continuam custando dinheiro todo mês. Este
projeto simula uma rotina de auditoria que:

1. Lê os dados de usuários exportados de um “Admin Center”
2. Identifica quem está inativo com base na data do último login
3. Calcula quanto a empresa economizaria revogando essas licenças
4. Entrega isso em um relatório Excel pronto para decisão

## Status atual

| Etapa                              | Status |
|-----------------------------------|--------|
| Estrutura do projeto               | ✅ Concluído |
| Leitura de dados (CSV)             | ✅ Concluído |
| Limpeza de dados                   | ✅ Concluído |
| Processamento (status + economia)  | ✅ Concluído |
| Geração de relatório Excel          | ✅ Concluído |
| Automação de extração (Selenium)    | ✅ Concluído |
| Ambiente de teste Flask (mock_server) | ✅ Concluído |
| Envio de alerta por e‑mail          | 🔜 Planejado |
| Agendamento automático              | 🔜 Planejado |
| Testes automatizados (pytest)      | 🔜 Planejado |

## Arquitetura

O pipeline segue um fluxo linear, onde cada etapa é uma função isolada,
testável independentemente, que recebe o resultado da etapa anterior:

```
data/raw/usuarios_admin_center.csv
        │
        ▼
   read_data_users()                → DataFrame bruto
        │
        ▼
   clean_user_data()                → nomes e‑mails corrigidos
        │
        ▼
   process_user_data()               → status (ativo/alerta/inativo) + economia
        │
        ▼
   export_report() (report_writer.py) → data/processed/relatorio_smartlicense.xlsx
```

### Estrutura de pastas

```
smartlicense-rpa/
├── data/
│   ├── raw/              # dado bruto, nunca editado manualmente
│   └── processed/        # relatórios gerados (Excel)
├── src/
│   ├── data_reader.py          # lê o CSV
│   ├── data_cleaner.py         # corrige nomes/e‑mails malformados
│   ├── data_analysis.py       # calcula status e economia
│   ├── report_writer.py        # gera o Excel (aba Resumo + aba Detalhes)
│   └── web_automation.py       # Selenium: login + extração via extract_users_from_portal()
├── mock_server/
│   ├── app.py                  # Flask mock server (rotas /login e /dashboard)
│   └── templates/             # login.html, dashboard.html
├── logs/
│   ├── execution/              # logs de cada execução do robô
│   └── screenshots/           # evidências visuais (Selenium)
├── config/                     # variáveis de ambiente e credenciais (.env)
├── tests/                      # testes automatizados (pytest) – ainda vazio
├── main.py                     # ponto de entrada — orquestra o pipeline
├── gerar_dados_simulados.py
├── requirements.txt
└── README.md
```

## Diagrama Mermaid (fluxo de dados completo)

```mermaid
flowchart LR
    A[CSV (raw)] -->|read_data_users| B[DataFrame bruto]
    B -->|clean_user_data| C[DataFrame limpo]
    C -->|process_user_data| D[DataFrame final]
    D -->|export_report (report_writer.py)| E[Relatório Excel]

    subgraph UI
        F[Flask mock_server] -->|render dashboard| G[HTML tabela]
        G -->|Selenium| H[extract_users_from_portal (web_automation.py)]
    end
    H --> I[Lista de dicts (nome, email, status)]
    I -->|opcional| D
```


---

## Decisões técnicas relevantes

- **Nenhuma coluna de status pronta no dado bruto** – a inatividade é calculada a partir da data do último login, reforçando a lógica de negócio.
- **Limpeza de e‑mail por reconstrução** – o e‑mail é gerado a partir do nome já limpo, garantindo consistência.
- **`np.select` para classificação** – permite vetorização e legibilidade ao definir múltiplas categorias.

## Próximos passos

- Automatizar a extração de dados simulando login em um sistema via Selenium.
- Enviar o relatório por e‑mail automaticamente (`smtplib`).
- Agendar execuções recorrentes com a biblioteca `schedule`.
- Cobrir o pipeline com testes automatizados (`pytest`).

## Autor

**James Gustavo de Castro Fernandes**
Projeto desenvolvido como parte de estudos em Engenharia de Dados.
