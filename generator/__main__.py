from argparse import ArgumentParser

from .generator import main

parser = ArgumentParser(description="CLI for a Tiqets assignment")

parser.add_argument("-o", "--orders", type=str, required=False, default="data/orders.csv",
                    help="Path to the orders CSV file", dest="orders")
parser.add_argument("-b", "--barcodes", type=str, required=False, default="data/barcodes.csv",
                    help="Path to the barcodes CSV file", dest="barcodes")
parser.add_argument("-p", "--path", type=str, required=False, default="data/output.csv",
                    help="Path to the output CSV file", dest="path")

if __name__ == "__main__":
    ns = parser.parse_args()
    main(ns)
