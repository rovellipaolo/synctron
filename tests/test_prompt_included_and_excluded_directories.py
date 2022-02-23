import unittest
from unittest.mock import patch

from synctron import prompt_included_and_excluded_directories


class TestPromptIncludedAndExcludedDirectories(unittest.TestCase):
    """
    Test prompt_included_and_excluded_directories method.
    """

    ANY_SOURCE = "any-source"
    ANY_DIRECTORY = "any-directory"
    ANY_OTHER_DIRECTORY = "any-other-directory"

    @patch('synctron.prompt_multiple_selection')
    @patch('synctron.listdir')
    def test_happy_case(
            self,
            mock_listdir,
            mock_prompt_multiple_selection
    ):
        mock_listdir.return_value = [self.ANY_DIRECTORY, self.ANY_OTHER_DIRECTORY]
        mock_prompt_multiple_selection.return_value = [self.ANY_DIRECTORY]

        included, excluded = prompt_included_and_excluded_directories(self.ANY_SOURCE)

        self.assertEqual([self.ANY_DIRECTORY], included)
        self.assertEqual([self.ANY_OTHER_DIRECTORY], excluded)
        mock_listdir.assert_called_once_with(self.ANY_SOURCE)
        mock_prompt_multiple_selection.assert_called_once_with(
            question="Select the source subdirectories to be backed up:",
            options = [self.ANY_DIRECTORY, self.ANY_OTHER_DIRECTORY]
        )

    @patch('synctron.listdir')
    def test_no_subdirectory_found(
            self,
            mock_listdir
    ):
        mock_listdir.return_value = []

        with self.assertRaises(SystemExit) as result:
            prompt_included_and_excluded_directories(self.ANY_SOURCE)

        self.assertEqual(1, result.exception.code)
        mock_listdir.assert_called_once_with(self.ANY_SOURCE)


if __name__ == '__main__':
    unittest.main()
