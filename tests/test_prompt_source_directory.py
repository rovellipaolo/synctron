import unittest
from unittest.mock import patch

from synctron import prompt_source_directory


class TestPromptSourceDirectory(unittest.TestCase):
    """
    Test prompt_source_directory method.
    """

    ANY_DIRECTORY = "any-directory"
    ANY_OTHER_DIRECTORY = "any-other-directory"

    @patch('synctron.prompt_single_selection')
    @patch('synctron.get_home_directories')
    def test_happy_case(self, mock_get_home_directories, mock_prompt_single_selection):
        mock_get_home_directories.return_value = [self.ANY_DIRECTORY, self.ANY_OTHER_DIRECTORY]
        mock_prompt_single_selection.return_value = self.ANY_DIRECTORY

        result = prompt_source_directory()

        self.assertEqual(self.ANY_DIRECTORY, result)
        mock_get_home_directories.assert_called_once()
        mock_prompt_single_selection.assert_called_once_with(
            question="Select the source directory to be backed up:",
            options=[self.ANY_DIRECTORY, self.ANY_OTHER_DIRECTORY]
        )

    @patch('synctron.get_home_directories')
    def test_no_home_directory_found(self, mock_get_home_directories):
        mock_get_home_directories.return_value = []

        with self.assertRaises(SystemExit) as result:
            prompt_source_directory()

        self.assertEqual(1, result.exception.code)
        mock_get_home_directories.assert_called_once()


if __name__ == '__main__':
    unittest.main()
