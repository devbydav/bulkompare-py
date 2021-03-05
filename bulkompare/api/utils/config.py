from typing import Optional

import logging
import pathlib

from pydantic import BaseModel

from api.utils.constants import home_dir

logger = logging.getLogger(__name__)


class ConfiguredModel(BaseModel):
    """Base model used as a base in the app"""
    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True
        validate_assignment = True


def import_gui_config(path: pathlib.Path):
    """Loads configuration when app starts"""
    if path.is_file():
        config = GuiConfig.parse_file(path)
        logger.debug(f"Config successfully loaded from {path}")
    else:
        # this usually happens if default is missing. If user selects a file from the dialog, it should exist
        logger.debug("Config not found, initializing it with hardcoded default")
        config = GuiConfig()

    config._path = path
    return config


class GuiConfig(ConfiguredModel):
    """Holds the configuration for the gui"""
    # config file
    _path: Optional[pathlib.Path] = None

    # path when opening a dialog for selecting csv file dir
    csv_dir: pathlib.Path = home_dir

    # path when opening a dialog for selecting a selection file
    selections_dir: pathlib.Path = pathlib.Path(__file__).parent

    custom: dict = dict()

    def __str__(self):
        return "GuiConfig"

    def __repr__(self):
        return f"GuiConfig(csv_dir={self.csv_dir}, selections_dir={self.selections_dir}, custom=...)"

    def save_to_file(self):
        """Saves configuration to file"""

        json_dump = self.json(indent=2)

        with open(self._path, "wt") as f:
            f.write(json_dump)

        logger.debug(f"Config saved to {self._path}")
