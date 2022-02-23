import unittest
from unittest.mock import Mock, patch

from synctron import run_rsync


class TestBuildRsyncCommand(unittest.TestCase):
    """
    Test run_rsync method.
    """

    ANY_COMMAND = "any-command"
    ANY_OUTPUT = "any-output"
    ANY_SOURCE = "any-source"
    ANY_DESTINATION = "any-destination"
    ANY_EXCLUDED = []
    ANY_DRY_RUN = True

    @staticmethod
    def any_completed_process(stdout: str) -> Mock:
        completed_process = Mock()
        completed_process.stdout = stdout
        return completed_process

    @patch('synctron.run')
    @patch('synctron.build_rsync_command')
    def test_happy_case(self, mock_build_rsync_command, mock_run):
        output = self.any_completed_process(stdout=self.ANY_OUTPUT)
        mock_run.return_value = output
        mock_build_rsync_command.return_value = self.ANY_COMMAND

        result = run_rsync(
            source=self.ANY_SOURCE,
            destination=self.ANY_DESTINATION,
            excluded=self.ANY_EXCLUDED,
            dry_run=self.ANY_DRY_RUN
        )

        self.assertEqual(output, result)
        mock_build_rsync_command.assert_called_once_with(
            self.ANY_SOURCE,
            self.ANY_DESTINATION,
            self.ANY_EXCLUDED,
            self.ANY_DRY_RUN
        )
        mock_run.assert_called_once_with(self.ANY_COMMAND, check=True, capture_output=True, text=True)


if __name__ == '__main__':
    unittest.main()
