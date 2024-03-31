import smtplib, ssl
import unittest
from unittest.mock import patch, ANY, MagicMock
from smail.connection.mail_connection import send_email



class TestSendEmail(unittest.TestCase):

    def setUp(self):
        self.recipient = "test@test.com"
        self.subject = "Test Subject"
        self.content = "Test Content"
        self.login = "ts1bp2023@gmail.com"
        self.password = "password"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    @patch("smtplib.SMTP")
    @patch("smail.connection.mail_connection.logger")
    def test_send_email_success(self, mock_logger, mock_smtp):
        result = send_email(self.recipient, self.subject, self.content, self.login, self.password, self.smtp_server,
                            self.smtp_port)
        mock_logger.error.assert_not_called()
        mock_logger.info.assert_called_once_with(f"An email has been sent to {self.recipient}.")
        mock_smtp.assert_called_with(self.smtp_server, self.smtp_port)
        self.assertEqual(result, 1)

    @patch("smtplib.SMTP", side_effect=smtplib.SMTPConnectError(421, "Test SMTPConnectError"))
    @patch("smail.connection.mail_connection.logger")
    def test_smtp_connect_error(self, mock_logger, mock_smtp):
        result = send_email(self.recipient, self.subject, self.content, self.login, self.password, self.smtp_server,
                            self.smtp_port)
        mock_smtp.assert_called_once_with(self.smtp_server, self.smtp_port)
        mock_logger.error.assert_called_once_with("SMTP connection error. Check your SMTP server and port.",
                     exc_info=True)
        mock_logger.info.assert_not_called()

        self.assertEqual(result, 0)

    @patch("smtplib.SMTP", side_effect=smtplib.SMTPAuthenticationError(535, "Test SMTPAuthenticationError"))
    @patch("smail.connection.mail_connection.logger")
    def test_smtp_authentication_error(self,mock_logger, mock_smtp):
        result = send_email(self.recipient, self.subject, self.content, self.login, self.password, self.smtp_server,
                            self.smtp_port)
        mock_smtp.assert_called_once_with(self.smtp_server, self.smtp_port)
        mock_logger.error.assert_called_once_with("Authentication error. Check your email and password.",
                     exc_info=True)
        mock_logger.info.assert_not_called()

        self.assertEqual(result, -1)

    @patch("smtplib.SMTP", side_effect = Exception("Test Exception"))
    @patch("smail.connection.mail_connection.logger")
    def test_exception_during_send_email(self,mock_logger, mock_smtp):
        result = send_email(self.recipient, self.subject, self.content, self.login, self.password, self.smtp_server, self.smtp_port)

        mock_smtp.assert_called_once_with(self.smtp_server, self.smtp_port)
        mock_logger.error.assert_called_once_with("Error occurred when trying to send email. ",
                     exc_info=True)
        mock_logger.info.assert_not_called()

        self.assertEqual(result, -2)

    if __name__ == '__main__':
        unittest.main()
