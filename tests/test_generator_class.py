import unittest

from pandas import DataFrame
from generator.generator import Generator


class TestGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.path = "data/test.csv"

    def test_generate_output_dataframe_empty(self):
        orders_data = []
        barcodes_data = []
        orders = DataFrame(orders_data, columns=["order_id", "customer_id"])
        barcodes = DataFrame(barcodes_data, columns=["barcode", "order_id"])
        correct_output = DataFrame([], columns=["customer_id", "order_id", "barcodes"])
        gt = Generator(orders, barcodes, self.path)
        output, empty = gt.generate_output_dataframe()

        self.assertTrue(correct_output.equals(output))
        self.assertEqual([], empty)

    def test_generate_output_dataframe_non_empty(self):
        orders_data = [[1, 10], [2, 11], [3, 12]]
        barcodes_data = [[11111111111, 1], [11111111112, 2], [11111111113, 4], [11111111114, 1]]
        orders = DataFrame(orders_data, columns=["order_id", "customer_id"])
        barcodes = DataFrame(barcodes_data, columns=["barcode", "order_id"])
        correct_output = DataFrame([[10, 1, [11111111111, 11111111114]], [11, 2, [11111111112]]],
                                   columns=["customer_id", "order_id", "barcodes"])
        gt = Generator(orders, barcodes, self.path)
        output, empty = gt.generate_output_dataframe()

        self.assertTrue(correct_output.equals(output))
        self.assertEqual([3, 4], empty)

    def test_generate_output_dataframe_no_empty_orders(self):
        orders_data = [[1, 10], [2, 11]]
        barcodes_data = [[11111111111, 1], [11111111112, 2]]
        orders = DataFrame(orders_data, columns=["order_id", "customer_id"])
        barcodes = DataFrame(barcodes_data, columns=["barcode", "order_id"])
        correct_output = DataFrame([[10, 1, [11111111111]], [11, 2, [11111111112]]],
                                   columns=["customer_id", "order_id", "barcodes"])
        gt = Generator(orders, barcodes, self.path)
        output, empty = gt.generate_output_dataframe()

        self.assertTrue(correct_output.equals(output))
        self.assertEqual([], empty)

    def test_check_unused_exists(self):
        gt = Generator(DataFrame(), DataFrame(), self.path)
        output = gt.check_unused({1, 2, 3}, {1, 2})
        correct_output = [3]
        self.assertEqual(correct_output, output)

    def test_check_unused_all_used(self):
        gt = Generator(DataFrame(), DataFrame(), self.path)
        output = gt.check_unused({1, 2, 3}, {1, 2, 3})
        correct_output = []
        self.assertEqual(correct_output, output)

    def test_check_unused_first_element_empty(self):
        gt = Generator(DataFrame(), DataFrame(), self.path)
        output = gt.check_unused(set(), {1, 2, 3})
        correct_output = []
        self.assertEqual(correct_output, output)

    def test_find_most_valuable_customers_more_than_one_count(self):
        df = DataFrame([[10, 1, [11111111111]], [11, 2, [11111111112]]],
                       columns=["customer_id", "order_id", "barcodes"])
        gt = Generator(DataFrame(), DataFrame(), self.path)
        output = gt.find_most_valuable_customers(df, 5)
        correct_df = DataFrame([[10, 1], [11, 1]], columns=["customer_id", "count"])
        self.assertTrue(correct_df.equals(output))

    def test_find_most_valuable_customers_less_than_output_count(self):
        df = DataFrame([[10, 1, [11111111111]], [11, 2, [11111111112]]],
                       columns=["customer_id", "order_id", "barcodes"])
        gt = Generator(DataFrame(), DataFrame(), self.path)
        output = gt.find_most_valuable_customers(df, 1)
        correct_df = DataFrame([[10, 1]], columns=["customer_id", "count"])
        self.assertTrue(correct_df.equals(output))

    def test_find_most_valuable_customers(self):
        df = DataFrame([[10, 1, [11111111111, 11111111113]], [11, 2, [11111111112]]],
                       columns=["customer_id", "order_id", "barcodes"])
        gt = Generator(DataFrame(), DataFrame(), self.path)
        output = gt.find_most_valuable_customers(df, 5)
        correct_df = DataFrame([[10, 2], [11, 1]], columns=["customer_id", "count"])
        self.assertTrue(correct_df.equals(output))
