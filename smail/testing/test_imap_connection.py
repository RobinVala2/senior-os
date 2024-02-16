import imaplib
import unittest
from unittest.mock import patch, MagicMock, ANY
from smail.connection.mail_connection import imap_connection

class TestImapConnection(unittest.TestCase):
    login = "ts1bp2023@gmail.com"
    password = "wuaxnflbzrdyysdy"
    imap_server = "smtp.gmail.com"
    imap_port = 993

    @patch("imaplib.IMAP4_SSL")
    def test_imap_connection_success(self, mock_imap4_ssl):
        mock_mail = MagicMock()
        mock_imap4_ssl.return_value = mock_mail
        result = imap_connection(self.login, self.password, self.imap_server, self.imap_port)
        mock_imap4_ssl.assert_called_once_with(self.imap_server, self.imap_port, ssl_context=ANY)
        mock_mail.login.assert_called_once_with(self.login, self.password)
        self.assertEqual(result, mock_mail)

    @patch("imaplib.IMAP4_SSL", side_effect=imaplib.IMAP4.error)
    def test_imap_connection_imap_error(self, mock_imap4_ssl):
        result = imap_connection(self.login, self.password, self.imap_server, self.imap_port)
        mock_imap4_ssl.assert_called_once_with(self.imap_server, self.imap_port, ssl_context=ANY)
        self.assertEqual(result, 0)

    @patch("imaplib.IMAP4_SSL", side_effect=ConnectionError)
    def test_imap_connection_connection_error(self, mock_imap4_ssl):
        result = imap_connection(self.login, self.password, self.imap_server, self.imap_port)
        mock_imap4_ssl.assert_called_once_with(self.imap_server, self.imap_port, ssl_context=ANY)
        self.assertEqual(result, -1)

    @patch("imaplib.IMAP4_SSL", side_effect=Exception)
    def test_imap_connection_unexpected_error(self, mock_imap4_ssl):
        result = imap_connection(self.login, self.password, self.imap_server, self.imap_port)
        mock_imap4_ssl.assert_called_once_with(self.imap_server, self.imap_port, ssl_context=ANY)
        self.assertEqual(result, -2)


if __name__ == '__main__':
    unittest.main()
