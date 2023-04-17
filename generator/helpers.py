from pandas import read_csv, DataFrame


def read_csv_file(path: str) -> DataFrame:
    """
    Reads CSV file
    :param path: path to the CSV file
    :return: pandas dataframe
    """
    return read_csv(path)
