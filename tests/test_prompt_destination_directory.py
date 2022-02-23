import unittest
from unittest.mock import patch

from synctron import prompt_destination_directory


class TestPromptDestinationDirectory(unittest.TestCase):
    """
    Test prompt_destination_directory method.
    """

    ANY_DESTINATION = "any-destination-root"
    ANY_DRIVE = "any-drive"
    ANY_OTHER_DRIVE = "any-other-drive"

    @patch('synctron.prompt_single_selection')
    @patch('synctron.get_mounted_drives')
    def test_happy_case(self, mock_get_mounted_drives, mock_prompt_single_selection):
        mock_get_mounted_drives.return_value = [self.ANY_DRIVE, self.ANY_OTHER_DRIVE]
        mock_prompt_single_selection.return_value = self.ANY_DRIVE

        result = prompt_destination_directory(self.ANY_DESTINATION)

        self.assertEqual(self.ANY_DRIVE, result)
        mock_get_mounted_drives.assert_called_once()
        mock_prompt_single_selection.assert_called_once_with(
            question="Select the destination directory to store the backup:",
            options = [
                f"{self.ANY_DRIVE}/{self.ANY_DESTINATION}",
                f"{self.ANY_OTHER_DRIVE}/{self.ANY_DESTINATION}"
            ]
        )

    @patch('synctron.get_mounted_drives')
    def test_no_mounted_drive_found(self, mock_get_mounted_drives):
        mock_get_mounted_drives.return_value = []

        with self.assertRaises(SystemExit) as result:
            prompt_destination_directory(self.ANY_DESTINATION)

        self.assertEqual(1, result.exception.code)
        mock_get_mounted_drives.assert_called_once()


if __name__ == '__main__':
    unittest.main()
