import logging
import pathlib

from api.csv_manager import CsvManager

logger = logging.getLogger(__name__)


def import_selection(path: pathlib.Path):
    """Loads selection from a file"""

    if not path.is_file():
        # this usually happens if default is missing. If user selects a file from the dialog, it should exist
        logger.debug("No default selection found, initializing CsvManager with hardcoded default")
        return CsvManager()

    logger.debug(f"reading {path}")
    manager = CsvManager.parse_file(path)

    return manager
