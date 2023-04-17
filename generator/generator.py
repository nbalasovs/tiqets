import sys
from argparse import Namespace
from pandas import DataFrame
from .helpers import read_csv_file, remove_duplicates


class Generator:
    def __init__(self, orders: DataFrame, barcodes: DataFrame, output_file_path: str) -> None:
        self.orders = orders
        self.barcodes = barcodes
        self.path = output_file_path


def main(ns: Namespace) -> None:
    """
    CLI entrypoint
    :param ns: argparse namespace
    :return:
    """
    orders = read_csv_file(ns.orders)
    barcodes = read_csv_file(ns.barcodes)
    deduplicated_barcodes, duplicates = remove_duplicates(barcodes, "barcode")

    for duplicate in duplicates:
        print(f"duplicate barcode: {int(duplicate)}", sys.stderr)
