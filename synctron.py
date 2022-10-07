#!/usr/bin/env python3

"""
Synctron: a simple home directory backup tool
"""

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
import logging
from os import listdir, makedirs, path
from pathlib import Path
from subprocess import run
import sys
import traceback
import psutil
import pyudev
from PyInquirer import prompt


logging.basicConfig(
    format="%(message)s",
    level=logging.INFO
)
logger: logging.Logger = logging.getLogger("Synctron")


DEFAULT_DESTINATION_ROOT_DIRECTORY = "backup"


def main():
    args = get_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    source = prompt_source_directory() if args.source is None else args.source
    logger.debug(f"Source directory: {source}")
    included, excluded = prompt_included_and_excluded_directories(source)
    logger.debug(f"Included directories: {included}")
    logger.debug(f"Excluded directories: {excluded}")

    destination = prompt_destination_directory(args.destination_root) if args.destination is None else args.destination
    logger.debug(f"Destination directory: {destination}")

    prompt_backup(source, destination, excluded=excluded)

    return 0


def prompt_source_directory() -> str:
    users = get_home_directories()
    if len(users) == 0:
        logger.error("No home directory could be found! Try to execute with '-v' option.")
        sys.exit(1)
    return prompt_single_selection(
        question="Select the source directory to be backed up:",
        options=users
    )


def prompt_included_and_excluded_directories(source: str) -> tuple:
    """
    NOTE: This will exclude both directories in the root and in subdirectories
    (e.g. "exclude" => "test/backup/user/excluded/" + "test/backup/user/NEW/excluded/")
    """
    directories = listdir(source)
    logger.debug(f"Subdirectories: {directories}")
    if len(directories) == 0:
        logger.error("No home subdirectory could be found! Try to execute with '-v' option.")
        sys.exit(1)
    included = prompt_multiple_selection(
        question="Select the source subdirectories to be backed up:",
        options=directories
    )
    excluded = [directory for directory in directories if not directory in included]
    return included, excluded


def prompt_destination_directory(destination) -> str:
    drives = get_mounted_drives()
    if len(drives) == 0:
        logger.error("No drive could be found! Try to execute with '-v' option.")
        sys.exit(1)
    return prompt_single_selection(
        question="Select the destination directory to store the backup:",
        options=[path.join(directory, destination) for directory in drives]
    )


def prompt_backup(source: str, destination: str, excluded: list):
    run_rsync(source, destination, excluded=excluded, dry_run=True)
    is_ok = prompt_confirmation("Are you sure to continue?")
    if is_ok:
        if not path.exists(destination):
            makedirs(destination)
        run_rsync(source, destination, excluded=excluded, dry_run=False)


def get_home_directories() -> list:
    dirs = []
    try:
        home = Path.home()
        for user in home.parent.iterdir():
            dirs.append(str(user))
    except RuntimeError:
        logger.debug(traceback.format_exc())
    logger.debug(f"Home directories: {dirs}")
    return dirs


def get_mounted_drives() -> list:
    devices = {}
    for device in pyudev.Context().list_devices(subsystem='block', DEVTYPE='partition'):
        devices[device.device_node] = device.get('ID_FS_LABEL', '-')
        logger.debug(f"Device: {device.device_node} ({device.get('ID_FS_LABEL', '-')}, {device.get('ID_FS_TYPE')})")
    drives = []
    for partition in psutil.disk_partitions():
        if partition.device in devices:
            drives.append(partition.mountpoint)
            logger.debug(f"Mounted: {partition.device} ({devices[partition.device]}) --> {partition.mountpoint}")
    return drives


def prompt_confirmation(question) -> bool:
    answers = prompt(
        [
            {
                "type": "confirm",
                "name": "choice",
                "message": question,
                "default": False
            }
        ]
    )
    return answers["choice"] if "choice" in answers else False


def prompt_single_selection(question: str, options: list) -> str:
    answers = prompt(
        [
            {
                "type": "list",
                "name": "choice",
                "message": question,
                "choices": options
            }
        ]
    )
    if "choice" not in answers:
        logger.error("Answer not found!")
        sys.exit(1)
    return answers["choice"]


def prompt_multiple_selection(question: str, options: list) -> list:
    answers = prompt(
        [
            {
                "type": "checkbox",
                "name": "choices",
                "message": question,
                "choices": [
                    {"name": option, "checked": not option.startswith('.')} for option in options
                ]
            }
        ]
    )
    return answers["choices"] if "choices" in answers else []


def build_rsync_command(source: str, destination: str, excluded: list, dry_run: bool=True) -> list:
    # -a, --archive           archive mode; equals -rlptgoD (no -H,-A,-X)
    # -c, --checksum          skip based on checksum, not mod-time & size
    # --exclude = PATTERN     exclude files matching PATTER
    # -E, --executability     preserve executability
    # -h, --human-readable    output numbers in a human-readable format
    # -i, --itemize-change    output a change-summary for all updates
    # -n --dry-run            perform a trial run with no changes made
    # -v, --verbose           increase verbosity
    # -X, --xattrs            preserve extended attributes
    command = ["rsync", "-acEhivX", "--delete"]
    if dry_run:
        command.append("--dry-run")
    for directory in excluded:
        command.append("--exclude")
        command.append(directory)
    command.append(source)
    command.append(destination)
    return command


def run_rsync(source: str, destination: str, excluded: list, dry_run: bool=True) -> str:
    command = build_rsync_command(source, destination, excluded, dry_run)
    logger.debug(f"Execute: {' '.join(command)}")
    output = run(command, check=True, capture_output=True, text=True)
    if output.stdout is not None and output.stdout != "":
        logger.info("Output: %s", output.stdout)
    if output.stderr is not None and output.stderr != "":
        logger.error("Error: %s", output.stderr)
    return output


def get_args() -> Namespace:
    parser = ArgumentParser(
        description="Synctron: a simple home directory backup tool built on top of rsync\n\n"
                    "examples:\n"
                    "  $ %(prog)s\n"
                    "  $ %(prog)s -dr backup\n"
                    "  $ %(prog)s -s test/home/user/ -d test/backup/user/\n"
                    "  $ %(prog)s --help\n",
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        action="store",
        dest="source",
        default=None,
        help="The source directory to be backed up, asked in a run-time prompt if missing"
    )
    parser.add_argument(
        "-d",
        "--destination",
        type=str,
        action="store",
        dest="destination",
        default=None,
        help="The destination directory to store the backup, asked in a run-time prompt if missing"
    )
    parser.add_argument(
        "-dr",
        "--destination-root",
        type=str,
        action="store",
        dest="destination_root",
        default=DEFAULT_DESTINATION_ROOT_DIRECTORY,
        help=f"The root for the destination directory, when this is asked in the run-time prompt"
             f"(default: '{DEFAULT_DESTINATION_ROOT_DIRECTORY}')"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="Show verbose logs"
    )
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
