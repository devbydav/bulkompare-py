import logging
from typing import Optional, Set, Dict, Tuple, List

import pandas as pd
from pydantic import validator

from api.utils.config import ConfiguredModel
from api.utils.constants import *
from api.utils.helpers import log_time_it
from api.utils.exceptions import StopError


logger = logging.getLogger(__name__)


class CsvSet(ConfiguredModel):
    status: Status = Status.INITIALIZED
    extension: str
    name: str
    directory: Optional[pathlib.Path]
    encoding: str = DEFAULT_ENCODING
    comment: str = DEFAULT_COMMENT
    skip_blank_lines: bool = DEFAULT_SKIP_BLANK
    header: int = DEFAULT_HEADER
    separator: str = DEFAULT_SEPARATOR

    # remove whitespace at beginning/end of every field
    strip: Optional[bool] = DEFAULT_STRIP

    # Mapping (dict key is name in csv, value is new name for dataset)
    mapping: Dict[str, str] = {}

    # Columns that will create the new index to id the lines, after renaming
    index_columns: Set[str]

    # Columns that will be compared between two sets, after renaming
    compare_columns: Set[str]

    # Columns imported for later display, not compared, after renaming (list for order)
    display_columns: List[str]

    # Generated later
    files: Tuple[pathlib.Path, ...] = tuple()
    original_columns: Tuple[str, ...] = tuple()  # columns available in all csv files (ordered)
    original_columns_set: Set[str] = set()  # same, as a set for efficient search
    renamed_columns: Tuple[str, ...] = tuple()  # all orginal columns renamed according to mapping
    renamed_columns_set: Set[str] = set()  # same, as a set
    df: Optional[pd.DataFrame] = None  # full set of data

    @validator('comment')
    def validate_comment(cls, v):
        return v or None

    @validator('separator')
    def validate_separator(cls, v):
        return v or "\t"

    def __str__(self):
        return f"CsvSet {self.name}"

    def update_sources(self, name:  str, directory: pathlib.Path):
        """Updates the names and source directories of data sets. Assumes directories exist"""
        self.force_status(Status.INITIALIZED)
        self.name = name
        self.directory = directory
        self.upgrade_status(target=Status.FILES_SELECTED)  # raise exception if we can't get to FILES_SELECTED

    def update_properties(self,
                          encoding: str,
                          skip_blank_line: bool,
                          comment: str,
                          header: int,
                          separator: str,
                          strip: bool):
        """Updates the csv set properties"""
        # Status goes down to initial
        self.force_status(min(self.status, Status.FILES_SELECTED))  # no need to revalidate before FILES_SELECTED
        self.status = Status.INITIALIZED
        self.skip_blank_lines = skip_blank_line
        self.encoding = encoding
        self.comment = comment
        self.header = header
        self.separator = separator
        self.strip = strip
        self.upgrade_status(target=Status.COLUMNS_AVAILABLE)  # raise exception if we can't get to COLUMNS_AVAILABLE

    def update_mapping(self, new: Dict[str, str]):
        """Updates the csv set mapping"""
        self.force_status(min(self.status, Status.COLUMNS_AVAILABLE))  # no need to revalidate before COLUMNS_AVAILABLE
        self.mapping = new
        self.upgrade_status(target=Status.MAPPING_VALID)  # raise exception if we can't get to MAPPING_VALID

    def update_selected_columns(self,
                                index_columns: Set[str],
                                compare_columns: Set[str],
                                display_columns: List[str]):
        """Updates the column selected for index, compare and display"""
        self.force_status(min(self.status, Status.MAPPING_VALID))  # any status above MAPPING VALID must be revalidated
        self.index_columns = index_columns
        self.compare_columns = compare_columns
        self.display_columns = display_columns
        self.upgrade_status(Status.READY_TO_IMPORT)  # raise exception if we can't get to READY_TO_IMPORT

    def force_status(self, new=Status.INITIALIZED):
        """Resets the status to the provided one"""
        self.status = new

    def upgrade_status_silently(self):
        """
            Upgrades the status to highest valid status without raising StopError.
            It doesn't revalidate the current status.
        """
        try:
            self.upgrade_status()
        except StopError as e:
            logger.debug(e)
        logger.debug(f"\tCsvSet {self.extension}/{self.name} status updated to {self.status}")

    def upgrade_status(self, target=Status.READY_TO_IMPORT):
        """
            Upgrades the status of csv set. Raises StopError when status can't be upgraded to status_target.
            It doesn't revalidate the current status.
        """

        if self.status == Status.INITIALIZED and target > Status.INITIALIZED:
            # => Check that some files are available
            if not self.directory:
                raise StopError(f"Aucun chemin spécifié pour {self.name}")

            if not self.directory.is_dir():
                raise StopError(f"Le répertoire {self.directory} n'existe pas ({self.name})")

            # reset list of files
            self.files = tuple(self.directory.glob(f"*.{self.extension}"))

            if not self.files:
                raise StopError(f"Aucun fichier {self.extension} trouvé dans {self.name}")

            self.status = Status.FILES_SELECTED

        if self.status == Status.FILES_SELECTED and target > Status.FILES_SELECTED:
            # => Check that some columns are available in each set
            # get the list of available columns
            common_columns = tuple()
            for i, file in enumerate(self.files):
                cols_in_this_file = tuple(self._read_csv(file, nrows=0).columns.tolist())
                if i == 0:
                    common_columns = cols_in_this_file
                else:
                    common_columns = (col for col in common_columns if col in cols_in_this_file)
            self.original_columns = tuple(common_columns)
            self.original_columns_set = set(self.original_columns)
            self.renamed_columns = tuple()
            self.renamed_columns_set = set()

            if not common_columns:
                raise StopError(f"Aucune colonne commune dans les fichiers csv {self.name}")

            self.status = Status.COLUMNS_AVAILABLE

        if self.status == Status.COLUMNS_AVAILABLE and target > Status.COLUMNS_AVAILABLE:
            # => Check that the mapping is valid
            if not set(self.mapping).issubset(self.original_columns_set):
                raise StopError(f"Les colonnes à renommer ne sont pas toutes disponibles dans {self.name} ")

            self.renamed_columns = tuple(self.mapping.get(col, col) for col in self.original_columns)
            self.renamed_columns_set = set(self.renamed_columns)

            self.status = Status.MAPPING_VALID

        if self.status == Status.MAPPING_VALID and target > Status.MAPPING_VALID:
            # => check that we are ready to import data
            # check that selection has been made
            if not self.index_columns:
                raise StopError(f"Aucune colonne sélectionnée pour indexer {self.name}")
            if not self.compare_columns:
                raise StopError(f"Aucune colonne sélectionnée pour comparaison dans {self.name}")
            if not self.display_columns:
                raise StopError(f"Aucune colonne sélectionnée pour l'affichage dans {self.name}")

            # check that selection is valid
            if not self.index_columns.issubset(self.renamed_columns_set):
                raise StopError(f"Les colonnes index ne sont pas toutes disponibles dans {self.name}")
            if not self.compare_columns.issubset(self.renamed_columns_set):
                raise StopError(f"Les colonnes à comparer ne sont pas toutes disponibles dans {self.name}")
            if not set(self.display_columns).issubset(self.renamed_columns_set):
                raise StopError(f"Les colonnes à afficher ne sont pas toutes disponibles dans {self.name}")

            # it doesn't make sense to compare columns selected for index
            if self.index_columns & self.compare_columns:
                raise StopError(f"Certaines colonnes sont sélectionnées en index et comparaison dans {self.name}")

            self.status = Status.READY_TO_IMPORT

    @log_time_it
    def import_data(self):
        """Imports the data from csv files, raises CsvSetError"""

        if not self.status >= Status.READY_TO_IMPORT:
            raise StopError(f"{self.name} n'est pas prêt pour l'import")

        # import all csv full files
        usecols = self.index_columns.union(self.compare_columns, self.display_columns)
        raw_dfs = [self._read_csv(f, usecols=usecols, dtype=str) for f in self.files]
        self.df = pd.concat(raw_dfs, ignore_index=True, sort=False)
        self.df.fillna("", inplace=True)

        if self.strip:
            # remove whitespace
            self.df = self.df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        if self.mapping:
            # rename df columns
            self.df.rename(columns=self.mapping, inplace=True)

        # set index (sort columns alphabetically in case both sets columns are not in same order
        sorted_index_cols = sorted(list(self.index_columns))
        self.df[NEW_INDEX] = self.df[sorted_index_cols].apply(lambda args: "-".join(args), axis=1)

        self.df[SET_NAME] = self.name

        self.status = Status.DATA_IMPORTED

    def _read_csv(self, file, usecols=None, nrows=None, na_values=None, dtype=None):
        return pd.read_csv(file,
                           engine="python",
                           index_col=False,
                           usecols=usecols,
                           na_values=na_values,
                           dtype=dtype,
                           encoding=self.encoding,
                           sep=self.separator,
                           header=self.header,
                           comment=self.comment,
                           skip_blank_lines=self.skip_blank_lines,
                           nrows=nrows)
