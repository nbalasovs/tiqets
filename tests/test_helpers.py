import unittest

from pandas import DataFrame
from generator.helpers import read_csv_file, flatten, remove_duplicates


class TestHelpers(unittest.TestCase):
    def setUp(self) -> None:
        self.correct_file_path = "data/orders.csv"
        self.incorrect_file_path = "file/path.csv"

    def test_read_csv_file_not_found(self):
        self.assertRaises(FileNotFoundError, read_csv_file, self.incorrect_file_path)

    def test_read_csv_file_found(self):
        try:
            read_csv_file(self.correct_file_path)
        except FileNotFoundError:
            self.fail("exception was raised with correct file path")

    def test_flatten_empty_list(self):
        output = flatten([])
        correct_output = []
        self.assertEqual(correct_output, output)

    def test_flatten_one_element(self):
        output = flatten([[1, 2, 3]])
        correct_output = [1, 2, 3]
        self.assertEqual(correct_output, output)

    def test_flatten_multiple_elements(self):
        output = flatten([[1, 2], [3, 4]])
        correct_output = [1, 2, 3, 4]
        self.assertEqual(correct_output, output)

    def test_remove_duplicates_no_duplicates(self):
        df = DataFrame([[1, 2], [3, 4]], columns=["one", "two"])
        output, duplicates = remove_duplicates(df, "one")
        self.assertTrue(df.equals(output))
        self.assertEqual([], duplicates)

    def test_remove_duplicates(self):
        df = DataFrame([[1, 2], [1, 1], [3, 4]], columns=["one", "two"])
        correct_df = DataFrame([[3, 4]], columns=["one", "two"])
        output, duplicates = remove_duplicates(df, "one")
        self.assertTrue(correct_df.equals(output))
        self.assertEqual([1], duplicates)
