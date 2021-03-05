import logging
import pathlib
from typing import Tuple, Set, List

import pandas as pd
import numpy as np
from pydantic import validator

from api.utils.config import ConfiguredModel
from api.utils.helpers import log_time_it
from api.utils.constants import NEW_INDEX
from api.utils.exceptions import StopError
from api.utils.constants import SET_NAME, SET_ID
from api.csv_set import CsvSet
from api.result import Result


logger = logging.getLogger(__name__)


class CsvComparator(ConfiguredModel):
    extension: str
    names: Tuple[str, str]
    directories: Tuple[pathlib.Path, pathlib.Path]

    # Columns that will create the new index to id the lines, after renaming. Also used in CsvSet
    index_columns: Set[str] = set()

    # Columns that will be compared between two sets, after renaming. Also used in CsvSet
    compare_columns: Set[str] = set()

    # Columns imported for later display, not compared, after renaming (list for order). Also used in CsvSet
    display_columns: List[str] = []

    csv_sets: Tuple[CsvSet, CsvSet] = None, None

    # individual differences
    _differences_df = None

    # all lines from both sets
    _all_df = None

    # lines with index only in 1 set
    _in_one_df = None

    # lines with index in both sets
    _in_both_df = None

    # subsets of in_both: 1 index in each set -> comparable else -> not comparable
    _not_comparable_df = None
    _comparable_df = None

    # subset of comparable : lines with differences
    _to_compare_df = None

    # result
    result: Result = Result()

    @validator('csv_sets', pre=True, always=True)
    def validate_csv_set(cls, v, values):
        logger.debug("Validating a pair of csv sets")
        values_set_a = v[0] or {}
        values_set_b = v[1] or {}

        update_set_a = {
            "extension": values["extension"],
            "name": values["names"][0],
            "directory": values["directories"][0],
            "index_columns": values["index_columns"],
            "compare_columns": values["compare_columns"],
            "display_columns": values["display_columns"]
        }
        update_set_b = {**update_set_a, "name": values["names"][1], "directory": values["directories"][1]}

        values_set_a.update(update_set_a)
        values_set_b.update(update_set_b)

        return CsvSet(**values_set_a), CsvSet(**values_set_b)

    @property
    def differences_in_common_lines(self):
        return self._differences_df

    @property
    def in_one(self):
        return self._in_one_df

    @property
    def not_compared(self):
        return self._not_comparable_df

    @property
    def status(self):
        return min(self.csv_sets[0].status, self.csv_sets[1].status)

    def update_sources(self, names: Tuple[str, str], directories: Tuple[pathlib.Path, pathlib.Path]):
        """Updates the names and source directories of data sets. Assumes directories exist"""
        self.names = names
        self.directories = directories
        for i in range(2):
            self.csv_sets[i].update_sources(name=names[i], directory=directories[i])

    def update_selected_columns(self,
                                index_columns: Set[str],
                                compare_columns: Set[str],
                                display_columns: List[str]):
        """Updates the column selected for index, compare and display"""
        self.index_columns = index_columns
        self.compare_columns = compare_columns
        self.display_columns = display_columns
        for csv_set in self.csv_sets:
            csv_set.update_selected_columns(index_columns, compare_columns, display_columns)

    def upgrade_status_silently(self):
        """
            Upgrades the status to highest valid status without raising StopError.
            It doesn't revalidate the current status.
        """
        for csv_set in self.csv_sets:
            csv_set.upgrade_status_silently()

    def _prepare_for_comparison(self):
        """Checks if comparison can be done"""

        if (
                self.csv_sets[0].index_columns != self.index_columns or
                self.csv_sets[1].index_columns != self.index_columns or
                self.csv_sets[0].compare_columns != self.compare_columns or
                self.csv_sets[1].compare_columns != self.compare_columns or
                self.csv_sets[0].display_columns != self.display_columns or
                self.csv_sets[1].display_columns != self.display_columns
        ):
            raise StopError("Les colonnes sélectionnées sont différentes dans les deux sets")


    @log_time_it
    def compare(self):
        """Compares the datasets"""
        self._prepare_for_comparison()

        # prepare full dataframe (both sets)
        for i, csv_set in enumerate(self.csv_sets):
            csv_set.import_data()
            csv_set.df[SET_ID] = i
        self._all_df = pd.concat((csv_set.df for csv_set in self.csv_sets))

        # count unique set_id for each index : 1 -> index is in 1 set, 2 set_id -> it is in both sets
        # note : nunique is min 1 (each line has a set_id), max 2 (there are only 2 different set_id)
        grouped = self._all_df.groupby(by=[NEW_INDEX])
        grouped_nunique = grouped[SET_ID].nunique()
        in_one_indexes = grouped_nunique[grouped_nunique == 1].index.tolist()
        in_one_mask = self._all_df[NEW_INDEX].isin(in_one_indexes)

        self._in_one_df = self._all_df[in_one_mask].copy()
        self._in_both_df = self._all_df[~in_one_mask].copy()

        # clear self._all_df
        self._all_df = None

        self.result.nb_in_one = tuple(self._in_one_df[self._in_one_df[SET_ID] == i].shape[0] for i in range(2))

        self.result.nb_in_both = tuple(self._in_both_df[self._in_both_df[SET_ID] == i].shape[0] for i in range(2))

        # count number of lines for each index : 2 -> index is comparable, more -> not comparable
        # note : each index has at least 1 line of each set_id (lines from in_both), so if count is 2 it's one of each
        size = self._in_both_df.groupby(by=[NEW_INDEX]).size()
        not_comparable_indexes = size[size > 2].index.tolist()
        not_comparable_mask = self._in_both_df[NEW_INDEX].isin(not_comparable_indexes)

        self._not_comparable_df = self._in_both_df[not_comparable_mask].copy()
        self._comparable_df = self._in_both_df[~not_comparable_mask].copy()

        self.result.nb_not_comparable = [self._not_comparable_df[self._not_comparable_df[SET_ID] == i].shape[0]
                                         for i in range(2)]

        # clear self._in_both_df
        self._in_both_df = None

        nb_comparable = self._comparable_df.shape[0] // 2

        self._to_compare_df = self._comparable_df.drop_duplicates(self.compare_columns.union({NEW_INDEX}), keep=False)

        # clear self._comparable_df
        self._comparable_df = None

        self.result.nb_with_differences = self._to_compare_df.shape[0] // 2
        self.result.nb_identical = nb_comparable - self.result.nb_with_differences

        self._create_differences()
        self._create_result()
        self._prepare_for_display()

    def _create_differences(self):
        """Creates a dataframe with each invidual difference in "in_both"""
        full_dfs = []
        compare_dfs = []
        for i in range(2):
            df = self._to_compare_df[self._to_compare_df[SET_ID] == i].set_index(NEW_INDEX)
            full_dfs.append(df)
            df = df.filter({NEW_INDEX} | self.compare_columns).copy()
            df = df.sort_index()
            compare_dfs.append(df)

        dfa, dfb = compare_dfs

        if dfa.equals(dfb):
            self._differences_df = pd.DataFrame()
        else:
            # take care of np.nan != np.nan returning True
            mask_differences = (dfa != dfb) & ~(dfa.isnull() & dfb.isnull())
            stack = mask_differences.stack()
            changes = stack[stack]
            changes.index.names = ["id", "colonne"]
            differences_locations = np.where(mask_differences)
            lot_a_data = dfa.values[differences_locations]
            lot_b_data = dfb.values[differences_locations]
            self._differences_df = pd.DataFrame({self.csv_sets[0].name: lot_a_data, self.csv_sets[1].name: lot_b_data},
                                                index=changes.index)

            # add the display columns
            for column in self.display_columns:
                in_set_a = self._differences_df.index.get_level_values(0).map(full_dfs[0][column])
                in_set_b = self._differences_df.index.get_level_values(0).map(full_dfs[1][column])
                if in_set_a.tolist() == in_set_b.tolist():
                    self._differences_df[column] = in_set_a
                else:
                    self._differences_df[column] = in_set_a + " / " + in_set_b

            # clear self._to_compare_df
            self._to_compare_df = None

            self._differences_df.reset_index(inplace=True)

    def _prepare_for_display(self):
        """Prepares dataframes for display"""
        self._in_one_df = self._in_one_df.filter([NEW_INDEX, SET_NAME] + self.display_columns) \
            .sort_values(by=NEW_INDEX).reset_index(drop=True).copy()
        self._not_comparable_df = self._not_comparable_df[[NEW_INDEX, SET_NAME] + self.display_columns] \
            .sort_values(by=NEW_INDEX).reset_index(drop=True).copy()

    def _create_result(self):
        """Creates the Result of the comparison"""

        self.result.nb_differences = self._differences_df.shape[0]

        nb_in_one = sum(self.result.nb_in_one)

        if self.result.nb_differences == 0:
            self.result.conclusion = "aucune valeur différente trouvée"
            if nb_in_one > 0:
                self.result.conclusion += f" mais {nb_in_one} ligne(s) dans un set seulement"

        else:
            if self.result.nb_differences > 1:
                self.result.conclusion = f"{self.result.nb_differences} valeurs différentes trouvées"
            else:
                self.result.conclusion = f"1 valeur différente trouvée"
            if nb_in_one > 0:
                self.result.conclusion += f" et {nb_in_one} ligne(s) dans un set seulement"

        name_a, name_b = self.names
        self.result.details = (f"Nombre total de lignes : {self.csv_sets[0].df.shape[0]} dans {name_a}, "
                               f"{self.csv_sets[1].df.shape[0]} dans {name_b}",

                               f"Lignes présentes dans un seul lot : {self.result.nb_in_one[0]} dans {name_a}, "
                               f"{self.result.nb_in_one[1]} dans {name_b} "
                               "(ces lignes n'ont pas d'équivalents dans les deux sets et ne sont pas comparées)",

                               f"Lignes présentes dans les 2 lots : {self.result.nb_in_both[0]} dans {name_a}, "
                               f"{self.result.nb_in_both[1]} dans {name_b}",

                               f"-> dont ligne(s) à index non unique(s): {self.result.nb_not_comparable[0]} dans {name_a}, "
                               f"{self.result.nb_not_comparable[1]} dans {name_b} "
                               "(ces lignes ne peuvent pas être comparées)",

                               f"-> dont {self.result.nb_identical} ligne(s) identique(s)",

                               f"-> dont {self.result.nb_with_differences} ligne(s) avec différence(s)")
