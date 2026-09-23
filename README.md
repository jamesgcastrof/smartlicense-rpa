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
Salesforce, VPN, etc.) atribuídas a colaboradores que pararam de usá-las
há meses — contas inativas continuam custando dinheiro todo mês. Esse
projeto simula uma rotina de auditoria que:

1. Lê os dados de usuários exportados de um "Admin Center"
2. Identifica quem está inativo com base na data do último login
3. Calcula quanto a empresa economizaria revogando essas licenças
4. Entrega isso em um relatório Excel pronto para decisão

## Status atual

| Etapa | Status |
|---|---|
| Estrutura do projeto | ✅ Concluído |
| Leitura de dados (CSV) | ✅ Concluído |
| Limpeza de dados | ✅ Concluído |
| Processamento (status + economia) | ✅ Concluído |
| Geração de relatório Excel | ✅ Concluído |
| Automação de extração (Selenium) | 🔜 Planejado |
| Envio de alerta por e-mail | 🔜 Planejado |
| Agendamento automático | 🔜 Planejado |
| Testes automatizados (pytest) | 🔜 Planejado |

## Arquitetura

O pipeline segue um fluxo linear, onde cada etapa é uma função isolada,
testável independentemente, que recebe o resultado da etapa anterior:

```
data/raw/usuarios_admin_center.csv
            │
            ▼
   read_data_users()          → DataFrame bruto
            │
            ▼
   clean_user_data()          → nomes e e-mails corrigidos
            │
            ▼
   process_user_data()        → status (ativo/alerta/inativo) + economia
            │
            ▼
   export_report()            → data/processed/relatorio_smartlicense.xlsx
```

### Por que essa separação em funções pequenas?

Cada função tem uma única responsabilidade e um contrato claro (o que
recebe, o que devolve). Isso significa que:

- Cada etapa pode ser testada isoladamente com `pytest`, sem precisar
  rodar o pipeline inteiro.
- Se a fonte de dados mudar (por exemplo, de um CSV exportado manualmente
  para uma chamada de API), apenas `read_data_users` precisa mudar — o
  resto do pipeline continua funcionando sem alteração.
- Bugs ficam mais fáceis de isolar: um problema no cálculo de economia
  não se confunde com um problema na limpeza de e-mails, porque são
  funções (e arquivos) diferentes.

### Estrutura de pastas

```
smartlicense-rpa/
├── data/
│   ├── raw/              # dado bruto, nunca editado manualmente
│   └── processed/        # relatórios gerados (Excel)
├── src/
│   ├── data_reader.py    # lê o CSV
│   ├── data_cleaner.py   # corrige nomes/e-mails malformados
│   ├── data_analysis.py  # calcula status e economia
│   └── report_export.py  # gera o Excel (aba Resumo + aba Detalhes)
├── logs/
│   ├── execution/        # logs de cada execução do robô
│   └── screenshots/      # evidências visuais (Selenium, Dia 2)
├── config/                # variáveis de ambiente e credenciais (.env)
├── tests/                 # testes automatizados (pytest)
├── main.py                # ponto de entrada — orquestra o pipeline
└── requirements.txt
```

`data/` e `processed/` nunca são versionados com dados reais no Git — só
a estrutura de pastas é mantida, e o CSV de exemplo é gerado por um
script auxiliar (ver abaixo), garantindo que qualquer pessoa clonando o
repositório consiga reproduzir o ambiente.

## Como o dado de exemplo foi gerado

O arquivo `data/raw/usuarios_admin_center.csv` (500 usuários) foi criado
com a biblioteca [Faker](https://faker.readthedocs.io/) (`pt_BR`), com
seed fixa para reprodutibilidade, seguindo uma distribuição realista de
atividade:

- ~70% dos usuários ativos (login nos últimos 30 dias)
- ~20% em zona de alerta (31 a 90 dias sem login)
- ~10% inativos (mais de 90 dias sem login)

O dataset contém inconsistências propositais (nomes com títulos como
"Sr." ou "Dra." colados, gerando e-mails malformados no CSV original) —
isso simula a qualidade de dados real de uma exportação corporativa, e é
corrigido pelo módulo `data_cleaner.py`.

## Como rodar localmente

### Pré-requisitos

- Python 3.10+ (testado com 3.14)
- Google Chrome instalado (necessário a partir do Dia 2, para a
  automação com Selenium)

### Instalação

```bash
git clone https://github.com/jamesgcastrof/smartlicense-rpa.git
cd smartlicense-rpa
pip install -r requirements.txt
```

### Executando o pipeline

```bash
python main.py
```

Isso executa o fluxo completo (leitura → limpeza → processamento →
exportação) e gera o relatório em
`data/processed/relatorio_smartlicense.xlsx`, com duas abas:

- **Resumo**: total de usuários, contagem por status e economia anual
  potencial.
- **Detalhes**: tabela completa, linha por linha, com nome, e-mail,
  departamento, licença, status e economia individual.

## Decisões técnicas relevantes

Algumas escolhas de design deste projeto, documentadas aqui porque
fazem parte do raciocínio de engenharia, não só do resultado final:

- **Nenhuma coluna de status pronta no dado bruto** — a inatividade é
  calculada a partir da data de último login, para que o processamento
  em Pandas reflita uma regra de negócio real, não um simples filtro.
- **Limpeza de e-mail por reconstrução, não por correção de padrão** — em
  vez de tentar prever todos os formatos possíveis de sujeira num e-mail
  já quebrado, o e-mail é reconstruído a partir do nome já limpo. Isso
  ataca a causa raiz do problema, não o sintoma.
- **`np.select` para classificação em múltiplas categorias** — usado no
  lugar de várias condições `if/elif` encadeadas, por ser vetorizado
  (roda em toda a coluna de uma vez, sem loop) e mais legível para três
  ou mais categorias mutuamente exclusivas.
- **Escrita do Excel dentro de um `with pd.ExcelWriter(...)`** — garante
  que o arquivo seja salvo de forma íntegra mesmo se ocorrer um erro no
  meio da escrita, evitando um relatório de auditoria financeira
  parcialmente gravado.

## Próximos passos

- Automatizar a extração de dados simulando login em um sistema via
  Selenium.
- Enviar o relatório por e-mail automaticamente (`smtplib`).
- Agendar execuções recorrentes com a biblioteca `schedule`.
- Cobrir o pipeline com testes automatizados (`pytest`).

## Autor

**James Gustavo de Castro Fernandes**
Projeto desenvolvido como parte de estudos em Engenharia de Dados.