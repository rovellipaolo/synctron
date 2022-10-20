import unittest
from parameterized import parameterized

from synctron import build_rsync_command


# pylint: disable=too-many-arguments
class TestBuildRsyncCommand(unittest.TestCase):
    """
    Test build_rsync_command method.
    """

    # pylint: disable=line-too-long
    @parameterized.expand([
        [
            "any-source",
            "any-destination",
            [],
            False,
            ["rsync", "-acEhivX", "--delete", "any-source", "any-destination"]
        ],
        [
            "any-source",
            "any-destination",
            [],
            True,
            ["rsync", "-acEhivX", "--delete", "--dry-run", "any-source", "any-destination"]
        ],
        [
            "any-source",
            "any-destination",
            ["any-excluded"],
            False,
            ["rsync", "-acEhivX", "--delete", "--exclude", "any-excluded", "any-source", "any-destination"]
        ],
        [
            "any-source",
            "any-destination",
            ["any-excluded"],
            True,
            ["rsync", "-acEhivX", "--delete", "--dry-run", "--exclude", "any-excluded", "any-source", "any-destination"]
        ],
        [
            "any-source",
            "any-destination",
            ["any-excluded", "any-other-excluded"],
            False,
            [
                "rsync",
                "-acEhivX",
                "--delete",
                "--exclude",
                "any-excluded",
                "--exclude",
                "any-other-excluded",
                "any-source",
                "any-destination"
            ]
        ],
        [
            "any-source",
            "any-destination",
            ["any-excluded", "any-other-excluded"],
            True,
            [
                "rsync",
                "-acEhivX",
                "--delete",
                "--dry-run",
                "--exclude",
                "any-excluded",
                "--exclude",
                "any-other-excluded",
                "any-source",
                "any-destination"
            ]
        ],
    ])
    def test_build(
            self,
            any_source,
            any_destination,
            any_excluded,
            any_dry_run,
            expected
    ):
        result = build_rsync_command(
            source=any_source,
            destination=any_destination,
            excluded=any_excluded,
            dry_run=any_dry_run
        )

        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
