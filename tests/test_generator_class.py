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
