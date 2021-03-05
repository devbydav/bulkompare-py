import pathlib
import logging
from typing import Optional, List, Tuple

from pydantic import validator

from api.utils.config import ConfiguredModel
from api.utils.constants import Status, home_dir
from api.csv_comparator import CsvComparator
from api.utils.exceptions import StopError

logger = logging.getLogger(__name__)


class CsvManager(ConfiguredModel):
    """Top-level class of the API. Manages all CsvComparator"""
    names: Tuple[str, str] = "Set A", "Set B"
    directories: Tuple[pathlib.Path, pathlib.Path] = home_dir, home_dir
    comparators: List[CsvComparator] = []
    results: Optional[dict] = None
    differences: Optional[dict] = None
    in_one: Optional[dict] = None
    not_compared: Optional[dict] = None

    @validator('comparators', pre=True, always=True, each_item=True)
    def validate_csv_comparator(cls, v, values):
        logger.debug("Validating a comparator")
        return CsvComparator(names=values["names"], directories=values["directories"], **v)

    @property
    def display_columns(self):
        return {comp.extension: comp.csv_sets[0].display_columns for comp in self.comparators}

    @property
    def compare_columns(self):
        return {comp.extension: comp.csv_sets[0].compare_columns for comp in self.comparators}

    @property
    def status(self):
        if self.comparators:
            return min(comp.status for comp in self.comparators)
        else:
            return Status.INITIALIZED

    def update_sources(self, names: Tuple[str, str], directories: Tuple[str, str], extensions: List[str]):
        """Sets the source to be compared"""
        self.directories = directories  # validator will convert to pathlib
        self.names = names

        for directory in self.directories:
            if not directory.is_dir():
                raise StopError(f"Le répertoire {directory.resolve()} n'existe pas")

        # add new extensions
        for extension in extensions:
            if all(comp.extension != extension for comp in self.comparators):
                logger.debug("Add new extension " + extension)
                self.comparators.append(CsvComparator(extension=extension,
                                                      names=self.names,
                                                      directories=self.directories))

        # remove extensions removed by user (iterate on a copy of keys as we might change the dict)
        for comp in self.comparators.copy():
            if comp.extension not in extensions:
                logger.debug("removing extention " + comp.extension)
                logger.debug("-> before " + str(self.comparators))
                self.comparators.remove(comp)
                logger.debug("-> after " + str(self.comparators))
                # del self.comparators[comp]

        # update comparators
        for comparator in self.comparators:
            comparator.update_sources(names, self.directories)

    def upgrade_status_silently(self):
        """
            Upgrades the status to highest valid status without raising StopError.
            It doesn't revalidate the current status.
        """
        for comparator in self.comparators:
            comparator.upgrade_status_silently()

        logger.info(f"Manager status updated to {self.status}")

    def compare(self):
        """Starts the comparisons"""
        for comparator in self.comparators:
            comparator.compare()

        self.results = {comp.extension: comp.result for comp in self.comparators}
        self.differences = {comp.extension: comp.differences_in_common_lines for comp in self.comparators}
        self.in_one = {comp.extension: comp.in_one for comp in self.comparators}
        self.not_compared = {comp.extension: comp.not_compared for comp in self.comparators}

    def save_selections(self, path=None):
        """Saves selections to a file"""

        if not path:
            path = pathlib.Path(__file__).resolve().parent.parent / "config" / "defaultTEST.json"

        json_dump = self.json(include={
            "names": ...,
            "directories": ...,
            "comparators": {"__all__": {
                "extension": ...,
                "index_columns": ...,
                "compare_columns": ...,
                "display_columns": ...,
                "csv_sets": {"__all__": {
                    "encoding": ...,
                    "comment": ...,
                    "skip_blank_lines": ...,
                    "header": ...,
                    "separator": ...,
                    "strip": ...,
                    "mapping": ...
                }}
            }}
        }, indent=2)

        with open(path, "w") as f:
            f.write(json_dump)

        logger.debug(f"Selections saved to {path}")