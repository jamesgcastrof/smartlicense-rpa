import pytest
from unittest.mock import patch
from src.email_notifier import send_alert_email


def test_send_alert_email_success(tmp_path):
    dummy_file = tmp_path / "dummy.txt"
    dummy_file.write_text("conteudo")

    with patch("smtplib.SMTP") as mock_smtp:
        instance = mock_smtp.return_value.__enter__.return_value
        send_alert_email(
            destinatario="test@example.com",
            assunto="Assunto",
            corpo="Corpo",
            anexo_path=str(dummy_file),
        )
        assert instance.send_message.called
        msg = instance.send_message.call_args[0][0]
        assert any(part.get_filename() == "dummy.txt" for part in msg.iter_attachments())


def test_send_alert_email_connection_error():
    with patch("smtplib.SMTP", side_effect=ConnectionRefusedError):
        with pytest.raises(RuntimeError):
            send_alert_email(
                destinatario="test@example.com",
                assunto="Assunto",
                corpo="Corpo",
                anexo_path=None,
            )
