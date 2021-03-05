import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from bulkompare.api.csv_manager import CsvManager


class TestComparison(unittest.TestCase):

    def setUp(self) -> None:
        self.manager = CsvManager.parse_file("data/selection.json")

    def test_comparison(self):

        self.manager.upgrade_status_silently()
        self.manager.compare()

        # check *.tsv differences (Empty and Val3 changed for Jane)
        expected = pd.DataFrame({
            "id": ["02/01/2021-Jane-08:20:23", "02/01/2021-Jane-08:20:23"],
            "colonne": ["Empty", "Val3"],
            "Before": ["", "5"],
            "After": ["Not empty", "6"],
            "Name": ["Jane", "Jane"],  # test display values that didn't change
            "Val3": ["5 / 6", "5 / 6"],  # test display values that changed
        })
        res = self.manager.differences["tsv"].sort_values(by="colonne").reset_index(drop=True)
        assert_frame_equal(expected, res, check_index_type=False)

        # check *.tsv in_one (Bob is only in set Before)
        expected = pd.DataFrame({
            "id": ["01/01/2021-Bob-08:20:23"],
            "set": ["Before"],
            "Name": ["Bob"],
            "Val3": ["5"],
        })
        assert_frame_equal(expected, self.manager.in_one["tsv"])

        # check *.tsv not_compared (Duplicate is in both sets twice)
        expected = pd.DataFrame({
            "id": ["01/01/2021-Duplicate-08:35:05"] * 4,
            "set": ["Before", "Before", "After", "After"],
            "Name": ["Duplicate"] * 4,
            "Val3": ["3"] * 4,
        })
        assert_frame_equal(expected, self.manager.not_compared["tsv"])

        # check *.other differences
        expected = pd.DataFrame({
            "id": ["02/01/2021-Henri-08:20:23"],
            "colonne": ["Val2"],
            "Before": ["5"],
            "After": [""],
            "Name": ["Henri"],
        })
        assert_frame_equal(expected, self.manager.differences["other"])

        # check *.other in_one (nothing)
        self.assertTrue(self.manager.in_one["other"].empty)

        # check *.other not_compared (nothing)
        self.assertTrue(self.manager.not_compared["other"].empty)
