from enum import Enum
import pathlib

NEW_INDEX = "id"
SET_NAME = "set"
SET_ID = "set_id"
home_dir = pathlib.Path.home()


class Status(Enum):
    INITIALIZED = 0
    FILES_SELECTED = 1
    COLUMNS_AVAILABLE = 2  # original columns names are read
    MAPPING_VALID = 3
    READY_TO_IMPORT = 4  # columns selected
    DATA_IMPORTED = 5

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


DEFAULT_ENCODING = "latin_1"
DEFAULT_HEADER = 2
DEFAULT_COMMENT = None
DEFAULT_SKIP_BLANK = False
DEFAULT_SEPARATOR = "\t"
DEFAULT_STRIP = True
