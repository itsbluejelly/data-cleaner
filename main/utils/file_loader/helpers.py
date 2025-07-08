import pandas as pd
from .schema import SUPPORTED_FILE_TYPES, SupportedFileType
from pathlib import Path
from typing import List, Sequence, Mapping, Literal, TypedDict


class LoadFileConfigParamType(TypedDict):
    """A type for the `config` param in the helper `load_file` function.

    Properties:
        1.`orient`:
        How to organize the data when serializing a DataFrame to JSON.

        2.`delimiter` (str):
        The delimiter to use when reading CSV or text files.

        3.`parse_dates`:
        A list of columns or a map of columns from which the date-values are converted to valid datetime strings
    """

    orient: Literal["records", "split", "index", "columns", "values", "table"]

    parse_dates: (
        List[str]
        | List[int]
        | Sequence[Sequence[int]]
        | Mapping[str, Sequence[int | str]]
    )

    delimiter: str


class WriteFileConfigParamType(TypedDict):
    """A type for the `config` param in the helper `write_file` function.

    Properties:
        1.`orient`:
        How to organize the data when serializing a DataFrame to JSON.

        2.`delimiter` (str):
        The delimiter to use when reading CSV or text files.
    """

    orient: Literal["records", "split", "index", "columns", "values", "table"]
    delimiter: str


def check_file_support(path: str) -> SupportedFileType:
    """A helper function that checks if the file type given is supported

    Args:
        path (str): The path to the file

    Raises:
        ValueError: If the file is not supported, currently only the file types below can be used
            1. Normal text files
            2. CSV files
            3. JSON files

    Returns:
        SupportedFileType: The supported file type
    """
    file_path = Path(path)
    file_extension = file_path.suffix.lower().removeprefix(".")

    if file_extension not in SUPPORTED_FILE_TYPES:
        raise ValueError(f"The file type {file_extension} is not supported")

    return file_extension


def load_file(path: str, config: LoadFileConfigParamType) -> pd.DataFrame:
    """A helper function that helps load data from a supported file to a valid pandas dataframe. If the file is not supported an error is thrown

    Args:
        path (str): The file path to read data from
        config (LoadFileConfigParamType): The config to use to customize the loaded data.

    Returns:
        pd.DataFrame: The dataframe loaded from the file
    """
    file_extension = check_file_support(path)

    if file_extension == "json":
        return pd.read_json(path, orient=config["orient"])
    else:
        return pd.read_csv(
            path,
            parse_dates=config["parse_dates"],
            delimiter=config["delimiter"],
        )


def write_file(path: str, data: pd.DataFrame, config: WriteFileConfigParamType):
    """A helper function to help write pandas data to supported files

    Args:
        path (str): The path to the file where the data is formatted to
        data (pd.DataFrame): The data to write as a dataframe
        config (WriteFileConfigParamType): The config to use to customize the loaded data.
    """
    file_path = check_file_support(path)

    if file_path == "json":
        data.to_json(path, orient=config["orient"])
    else:
        data.to_csv(path, sep=config["delimiter"])
