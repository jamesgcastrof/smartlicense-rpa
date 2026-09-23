import pandas as pd

def export_report(df_final: pd.DataFrame, output_path: str) -> None:
    """Grava o resumo e o detalhamento em um único arquivo Excel."""
    # 1️⃣ Resumo (contagem por status e economia total)
    status_counts = df_final["status"].value_counts()
    economia_total = df_final["economia_anual_inativo"].sum()

    resumo = pd.DataFrame({
        "Métrica": [
            "Total de usuários",
            "Ativos",
            "Em alerta",
            "Inativos",
            "Economia anual potencial (R$)",
        ],
        "Valor": [
            len(df_final),
            status_counts.get("ativo", 0),
            status_counts.get("alerta", 0),
            status_counts.get("inativo", 0),
            economia_total,
        ],
    })

    # 2️⃣ Escrita usando ExcelWriter (duas abas)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        resumo.to_excel(writer, sheet_name="Resumo", index=False)
        df_final.to_excel(writer, sheet_name="Detalhes", index=False)