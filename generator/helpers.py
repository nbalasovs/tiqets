from pandas import read_csv, DataFrame
from typing import Tuple


def read_csv_file(path: str) -> DataFrame:
    """
    Reads CSV file
    :param path: path to the CSV file
    :return: pandas dataframe
    """
    return read_csv(path)


def flatten(items: list) -> list:
    """
    Flattens list
    :param items: original list
    :return: flattened list
    """
    flattened = []
    for item in items:
        for elem in item:
            flattened.append(elem)
    return flattened


def remove_duplicates(data: DataFrame, key: str) -> Tuple[DataFrame, list]:
    """
    Removes duplicates from dataframe
    :param data: original dataframe
    :param key: column key based on which duplicates should be removed
    :return: cleaned dataframe and a list of duplicates
    """
    seen = {}
    for idx, item in data.iterrows():
        value = item[key]
        if value not in seen:
            seen[value] = [idx]
        else:
            seen[value].append(idx)

    duplicates = {k: v for k, v in seen.items() if len(v) > 1}
    indexes = flatten(list(duplicates.values()))

    return data.drop(indexes).reset_index(drop=True), list(duplicates.keys())
