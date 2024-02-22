import unittest
from unittest.mock import patch, mock_open
from smail.connection.style import load_json_file

class TestLoadJsonFile(unittest.TestCase):

    file_path = "../../sconf/SMAIL_config.json"

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_json_file_success(self, mock_open_file):
        result = load_json_file(self.file_path)
        mock_open_file.assert_called_once_with(self.file_path, "r")
        self.assertEqual(result, {"key": "value"})

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_json_file_file_not_found(self, mock_open_file):
        result = load_json_file(self.file_path)
        mock_open_file.assert_called_once_with(self.file_path, "r")
        self.assertEqual(result, 0)

    @patch("builtins.open", side_effect=Exception("Test unexpected error"))
    def test_load_json_file_unexpected_error(self, mock_open_file):
        result = load_json_file(self.file_path)
        mock_open_file.assert_called_once_with(self.file_path, "r")
        self.assertEqual(result, -1)


if __name__ == '__main__':
    unittest.main()
