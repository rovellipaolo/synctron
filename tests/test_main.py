from argparse import Namespace
from typing import Optional
import unittest
from unittest.mock import patch

from synctron import main


# pylint: disable=too-many-arguments
class TestMain(unittest.TestCase):
    """
    Test main method.
    """

    ANY_SOURCE = "any-source"
    ANY_DESTINATION = "any-destination"
    ANY_DESTINATION_ROOT = "any-destination-root"
    ANY_INCLUDED = ["any-included"]
    ANY_EXCLUDED = ["any-excluded"]

    @staticmethod
    def any_args(source: Optional[str], destination: Optional[str], destination_root: str) -> Namespace:
        args = Namespace()
        args.source = source
        args.destination = destination
        args.destination_root = destination_root
        args.verbose = False
        return args

    @patch('synctron.prompt_backup')
    @patch('synctron.prompt_destination_directory')
    @patch('synctron.prompt_included_and_excluded_directories')
    @patch('synctron.prompt_source_directory')
    @patch('argparse.ArgumentParser.parse_args')
    def test_happy_case(
            self,
            mock_parse_args,
            mock_prompt_source_directory,
            mock_prompt_included_and_excluded_directories,
            mock_prompt_destination_directory,
            mock_prompt_backup
    ):
        args = self.any_args(
            source=None,
            destination=None,
            destination_root=self.ANY_DESTINATION_ROOT
        )
        mock_parse_args.return_value = args
        mock_prompt_source_directory.return_value = self.ANY_SOURCE
        mock_prompt_included_and_excluded_directories.return_value = self.ANY_INCLUDED, self.ANY_EXCLUDED
        mock_prompt_destination_directory.return_value = self.ANY_DESTINATION

        main()

        mock_parse_args.assert_called_once()
        mock_prompt_source_directory.assert_called_once()
        mock_prompt_included_and_excluded_directories.assert_called_once_with(self.ANY_SOURCE)
        mock_prompt_destination_directory.assert_called_once_with(self.ANY_DESTINATION_ROOT)
        mock_prompt_backup.assert_called_once_with(self.ANY_SOURCE, self.ANY_DESTINATION, excluded=self.ANY_EXCLUDED)

    @patch('synctron.prompt_backup')
    @patch('synctron.prompt_destination_directory')
    @patch('synctron.prompt_included_and_excluded_directories')
    @patch('synctron.prompt_source_directory')
    @patch('argparse.ArgumentParser.parse_args')
    def test_happy_case_with_arguments(
            self,
            mock_parse_args,
            mock_prompt_source_directory,
            mock_prompt_included_and_excluded_directories,
            mock_prompt_destination_directory,
            mock_prompt_backup
    ):
        args = self.any_args(
            source=self.ANY_SOURCE,
            destination=self.ANY_DESTINATION,
            destination_root=self.ANY_DESTINATION_ROOT
        )
        mock_parse_args.return_value = args
        mock_prompt_included_and_excluded_directories.return_value = self.ANY_INCLUDED, self.ANY_EXCLUDED

        main()

        mock_parse_args.assert_called_once()
        mock_prompt_source_directory.assert_not_called()
        mock_prompt_included_and_excluded_directories.assert_called_once_with(self.ANY_SOURCE)
        mock_prompt_destination_directory.assert_not_called()
        mock_prompt_backup.assert_called_once_with(self.ANY_SOURCE, self.ANY_DESTINATION, excluded=self.ANY_EXCLUDED)


if __name__ == '__main__':
    unittest.main()
