"""
Função: send_alert_email
Envia um e‑mail de alerta (texto) usando um servidor SMTP local de teste (localhost:1025, sem autenticação).
Opcionalmente anexa um arquivo (p. ex. o relatório Excel gerado por report_writer).

Nota: Este servidor SMTP local sem autenticação é usado apenas para fins de teste e desenvolvimento. Em produção use um servidor SMTP autenticado (ex.: smtp.gmail.com na porta 587 com STARTTLS) cujas credenciais são carregadas de variáveis de ambiente via python‑dotenv — nunca hard‑coded.
"""
import os
import smtplib
from email.message import EmailMessage


def send_alert_email(
    destinatario: str,
    assunto: str,
    corpo: str,
    anexo_path: str | None = None,
) -> None:
    """Envia um e‑mail de alerta via SMTP local.

    Parameters
    ----------
    destinatario : str
        Endereço de e‑mail do destinatário.
    assunto : str
        Assunto da mensagem.
    corpo : str
        Corpo da mensagem em texto simples.
    anexo_path : str | None, optional
        Caminho absoluto ou relativo para um arquivo a ser anexado.
        Se ``None`` ou caminho inexistente, nenhum anexo é incluído.
    """
    msg = EmailMessage()
    msg["From"] = "smartlicense-rpa@teste.local"
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.set_content(corpo)

    if anexo_path and os.path.isfile(anexo_path):
        with open(anexo_path, "rb") as f:
            data = f.read()
        maintype, subtype = ("application", "octet-stream")
        filename = os.path.basename(anexo_path)
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)

    try:
        with smtplib.SMTP("localhost", 1025) as server:
            server.send_message(msg)
    except ConnectionRefusedError as exc:
        raise RuntimeError(
            "Não foi possível conectar ao servidor SMTP. "
            "Verifique se o servidor de teste está em execução "
            "(python -m aiosmtpd -n -l localhost:1025)."
        ) from exc


if __name__ == "__main__":
    # Exemplo de uso – o servidor aiosmtpd deve estar em execução:
    # python -m aiosmtpd -n -l localhost:1025
    relatorio = r"data\processed\relatorio_smartlicense.xlsx"
    anexo = relatorio if os.path.isfile(relatorio) else None
    send_alert_email(
        destinatario="destinatario@example.com",
        assunto="SmartLicense RPA - Relatório de Auditoria",
        corpo="Segue em anexo o relatório gerado pelo pipeline.",
        anexo_path=anexo,
    )
