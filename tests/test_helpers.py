import unittest

from generator.helpers import read_csv_file


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
