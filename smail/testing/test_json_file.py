import unittest
from unittest.mock import patch, mock_open
from smail.style import load_json_file

class TestLoadJsonFile(unittest.TestCase):

    def setUp(self):
        self.file_path = "../../sconf/SMAIL_config.json"

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_json_file_success(self, mock_open_file):
        result = load_json_file(self.file_path)
        mock_open_file.assert_called_once_with(self.file_path, "r")
        self.assertEqual(result, {"key": "value"})

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("smail.style.logger")
    def test_load_json_file_file_not_found(self, mock_logger, mock_open_file):
        result = load_json_file(self.file_path)
        mock_open_file.assert_called_once_with(self.file_path, "r")
        mock_logger.error.assert_called_once_with(f"File not found: {self.file_path}")
        self.assertEqual(result, 0)

    @patch("builtins.open", side_effect=Exception("Test unexpected error"))
    @patch("smail.style.logger")
    def test_load_json_file_unexpected_error(self, mock_logger, mock_open_file):
        result = load_json_file(self.file_path)
        mock_open_file.assert_called_once_with(self.file_path, "r")
        mock_logger.error.assert_called_once_with(f"An unexpected error occurred while loading data from {self.file_path}", exc_info=True)
        self.assertEqual(result, -1)

