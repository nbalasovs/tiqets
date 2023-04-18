import sys
from argparse import Namespace
from pandas import DataFrame
from typing import Tuple
from math import isnan
from .helpers import read_csv_file, remove_duplicates, flatten


class Generator:
    def __init__(self, orders: DataFrame, barcodes: DataFrame, output_file_path: str) -> None:
        self.orders = orders
        self.barcodes = barcodes
        self.path = output_file_path

    def generate_output_dataframe(self) -> Tuple[DataFrame, list]:
        """
        Converts barcodes and orders dataframes into appropriate format
        customer_id, order_id1, [barcode1, barcode2, ...]
        :return: dataframe in specified format and a list of empty orders
        """
        data_dict = {}
        # using outer strategy to merge since we want order ids from both orders and barcodes
        merged = self.orders.merge(self.barcodes, on="order_id", how="outer")
        merged_clean = merged.dropna()
        order_ids = [x for x in merged["order_id"].unique() if not isnan(x)]

        for _, item in merged_clean.iterrows():
            customer_id = int(item["customer_id"])
            order_id = int(item["order_id"])
            barcode = int(item["barcode"])

            if order_id not in data_dict:
                data_dict[order_id] = {"customer_id": customer_id, "barcodes": [barcode]}
            else:
                data_dict[order_id]["barcodes"].append(barcode)

        data = [[v["customer_id"], k, v["barcodes"]] for k, v in data_dict.items()]
        # check which order ids were left unused
        unused_order_ids = set(order_ids).difference(set(data_dict.keys()))

        return DataFrame(data, columns=["customer_id", "order_id", "barcodes"]), list(unused_order_ids)

    @staticmethod
    def check_unused(s1: set, s2: set) -> list:
        """
        Checks difference between sets s1 and s2
        :param s1: first set
        :param s2: second set
        :return: difference between sets
        """
        return list(s1.difference(s2))


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
        print(f"duplicate barcode: {int(duplicate)}", file=sys.stderr)

    gt = Generator(orders, deduplicated_barcodes, ns.path)
    df, unused_order_ids = gt.generate_output_dataframe()

    for idx in unused_order_ids:
        print(f"empty order: {int(idx)}", file=sys.stderr)

    # check only unique barcodes
    available_barcodes = set(deduplicated_barcodes["barcode"].to_list())
    valid_barcodes = set(flatten(df["barcodes"].to_list()))
    unused_barcodes = gt.check_unused(available_barcodes, valid_barcodes)

    print(f"number of unused barcodes: {len(unused_barcodes)}", file=sys.stdout)
