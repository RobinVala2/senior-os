import smtplib
import unittest
from unittest.mock import patch
from smail.connection.mail_connection import send_email

class TestSendEmail(unittest.TestCase):

    recipient = "test@test.com"
    subject = "Test Subject"
    content = "Test Content"
    login = "ts1bp2023@gmail.com"
    password = "password"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    @patch("smtplib.SMTP")
    @patch("smtplib.SMTP.starttls")
    @patch("smtplib.SMTP.login")
    @patch("smtplib.SMTP.sendmail")
    @patch("smail.connection.mail_connection.resend_reply")
    @patch("smail.connection.mail_connection.logger")
    def test_send_email_success(self, mock_logger, mock_resend_reply, mock_sendmail, mock_login, mock_starttls, mock_smtp):
        mock_server = mock_smtp.return_value
        mock_server.starttls.return_value = None
        mock_server.login.return_value = None
        mock_server.sendmail.return_value = None
        result = send_email(self.recipient, self.subject, self.content, self.login, self.password, self.smtp_server, self.smtp_port)
        mock_logger.error.assert_not_called()
        self.assertEqual(result, 1)

    @patch("smtplib.SMTP")
    def test_smtp_connect_error(self, mock_smtp):
        mock_smtp.side_effect = smtplib.SMTPConnectError(421, "Test SMTPConnectError")
        result = send_email(self.recipient, self.subject, self.content, self.login, self.password, self.smtp_server, self.smtp_port)
        self.assertEqual(result, 0)

    @patch("smtplib.SMTP")
    def test_smtp_authentication_error(self, mock_smtp):
        mock_smtp.side_effect = smtplib.SMTPAuthenticationError(535, "Test SMTPAuthenticationError")
        result = send_email(self.recipient, self.subject, self.content, self.login, self.password, self.smtp_server, self.smtp_port)
        self.assertEqual(result, -1)

    @patch("smtplib.SMTP")
    def test_exception_during_send_email(self, mock_smtp):
        mock_smtp.side_effect = Exception("Test Exception")
        result = send_email(self.recipient, self.subject, self.content, self.login, self.password, self.smtp_server, self.smtp_port)
        self.assertEqual(result, -2)

    if __name__ == '__main__':
        unittest.main()
