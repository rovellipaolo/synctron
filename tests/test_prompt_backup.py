import unittest
from unittest.mock import call, patch

from synctron import prompt_backup


# pylint: disable=too-many-arguments
class TestPromptBackup(unittest.TestCase):
    """
    Test prompt_backup method.
    """

    ANY_SOURCE = "any-source"
    ANY_DESTINATION = "any-destination"
    ANY_EXCLUDED = []

    @patch('synctron.path.exists')
    @patch('synctron.prompt_confirmation')
    @patch('synctron.run_rsync')
    def test_happy_case(
            self,
            mock_run_rsync,
            mock_prompt_confirmation,
            mock_path_exists
    ):
        mock_prompt_confirmation.return_value = True
        mock_path_exists.return_value = True

        prompt_backup(self.ANY_SOURCE, self.ANY_DESTINATION, self.ANY_EXCLUDED)

        mock_run_rsync.mock_path_exists(self.ANY_DESTINATION)
        mock_run_rsync.assert_has_calls([
            call(self.ANY_SOURCE, self.ANY_DESTINATION, excluded=self.ANY_EXCLUDED, dry_run=True),
            call(self.ANY_SOURCE, self.ANY_DESTINATION, excluded=self.ANY_EXCLUDED, dry_run=False),
        ])

    @patch('synctron.makedirs')
    @patch('synctron.path.exists')
    @patch('synctron.prompt_confirmation')
    @patch('synctron.run_rsync')
    def test_destination_directory_not_exist(
            self,
            mock_run_rsync,
            mock_prompt_confirmation,
            mock_path_exists,
            mock_makedirs
    ):
        mock_prompt_confirmation.return_value = True
        mock_path_exists.return_value = False

        prompt_backup(self.ANY_SOURCE, self.ANY_DESTINATION, self.ANY_EXCLUDED)

        mock_path_exists.assert_called_once_with(self.ANY_DESTINATION)
        mock_makedirs.assert_called_once_with(self.ANY_DESTINATION)
        mock_run_rsync.assert_has_calls([
            call(self.ANY_SOURCE, self.ANY_DESTINATION, excluded=self.ANY_EXCLUDED, dry_run=True),
            call(self.ANY_SOURCE, self.ANY_DESTINATION, excluded=self.ANY_EXCLUDED, dry_run=False),
        ])

    @patch('synctron.makedirs')
    @patch('synctron.path.exists')
    @patch('synctron.prompt_confirmation')
    @patch('synctron.run_rsync')
    def test_backup_not_confirmed(
            self,
            mock_run_rsync,
            mock_prompt_confirmation,
            mock_path_exists,
            mock_makedirs
    ):
        mock_prompt_confirmation.return_value = False

        prompt_backup(self.ANY_SOURCE, self.ANY_DESTINATION, self.ANY_EXCLUDED)

        mock_path_exists.assert_not_called()
        mock_makedirs.assert_not_called()
        mock_run_rsync.assert_has_calls([
            call(self.ANY_SOURCE, self.ANY_DESTINATION, excluded=self.ANY_EXCLUDED, dry_run=True)
        ])


if __name__ == '__main__':
    unittest.main()
