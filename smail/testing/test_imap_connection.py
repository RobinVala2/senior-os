import imaplib
import unittest
from unittest.mock import patch, MagicMock, ANY
from smail.connection.mail_connection import imap_connection

class TestImapConnection(unittest.TestCase):

    def setUp(self):
        self.login = "ts1bp2023@gmail.com"
        self.password = "password"
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993

    @patch("imaplib.IMAP4_SSL")
    @patch("smail.connection.mail_connection.logger")
    def test_imap_connection_success(self, mock_logger, mock_imap4_ssl):
        mock_mail = MagicMock()
        mock_imap4_ssl.return_value = mock_mail

        result = imap_connection(self.login, self.password, self.imap_server, self.imap_port)
        mock_imap4_ssl.assert_called_once_with(self.imap_server, self.imap_port, ssl_context=ANY)
        mock_mail.login.assert_called_once_with(self.login, self.password)
        mock_logger.info.assert_called_once_with("Successful connection to IMAP server.")
        mock_logger.error.assert_not_called()

        self.assertEqual(result, mock_mail)

    @patch("imaplib.IMAP4_SSL", side_effect=imaplib.IMAP4.error)
    @patch("smail.connection.mail_connection.logger")
    def test_imap_connection_imap_error(self,mock_logger, mock_imap4_ssl):
        result = imap_connection(self.login, self.password, self.imap_server, self.imap_port)
        mock_imap4_ssl.assert_called_once_with(self.imap_server, self.imap_port, ssl_context=ANY)
        mock_logger.error.assert_called_once_with("IMAP Error: Failed to connect to the IMAP server.", exc_info=True)
        mock_logger.info.assert_not_called()
        self.assertEqual(result, 0)

    @patch("imaplib.IMAP4_SSL", side_effect=ConnectionError)
    @patch("smail.connection.mail_connection.logger")
    def test_imap_connection_connection_error(self, mock_logger, mock_imap4_ssl):
        result = imap_connection(self.login, self.password, self.imap_server, self.imap_port)
        mock_imap4_ssl.assert_called_once_with(self.imap_server, self.imap_port, ssl_context=ANY)
        mock_logger.error.assert_called_once_with("Connection Error: Failed to establish a connection"
                     " to the IMAP server.", exc_info=True)
        mock_logger.info.assert_not_called()
        self.assertEqual(result, -1)

    @patch("imaplib.IMAP4_SSL", side_effect=Exception)
    @patch("smail.connection.mail_connection.logger")
    def test_imap_connection_unexpected_error(self, mock_logger, mock_imap4_ssl):
        result = imap_connection(self.login, self.password, self.imap_server, self.imap_port)
        mock_imap4_ssl.assert_called_once_with(self.imap_server, self.imap_port, ssl_context=ANY)
        mock_logger.error.assert_called_once_with("An unexpected error occurred. ", exc_info=True)
        mock_logger.info.assert_not_called()
        self.assertEqual(result, -2)

