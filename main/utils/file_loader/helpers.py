import pandas as pd
from .schema import SUPPORTED_FILE_TYPES, SupportedFileType
from pathlib import Path
from typing import List, Sequence, Mapping, Literal, TypedDict, NotRequired


class LoadFileConfigParamType(TypedDict):
    """A type for the `config` param in the helper loader file functions.

    **NB:** All properties are optional

    Properties:
        1.`orient`:
        How to organize the data when serializing a DataFrame to JSON.
        Default: "records"

        2.`delimiter` (str | None):
        The delimiter to use when reading CSV or text files.
        Default: ","

        3.`parse_dates`:
        A list of columns or a map of columns from which the date-values are converted to valid datetime strings
    """

    orient: NotRequired[
        Literal["records", "split", "index", "columns", "values", "table"]
    ]

    parse_dates: NotRequired[
        List[str]
        | List[int]
        | Sequence[Sequence[int]]
        | Mapping[str, Sequence[int | str]]
    ]

    delimiter: NotRequired[str]


class WriteFileConfigParamType(TypedDict):
    """A type for the `config` param in the helper loader file functions.

    **NB:** All properties are optional

    Properties:
        1.`orient`:
        How to organize the data when serializing a DataFrame to JSON.
        Default: "records"

        2.`delimiter` (str | None):
        The delimiter to use when reading CSV or text files.
        Default: ","
    """

    orient: NotRequired[
        Literal["records", "split", "index", "columns", "values", "table"]
    ]

    delimiter: NotRequired[str]


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


def load_file(path: str, config: LoadFileConfigParamType | None = None) -> pd.DataFrame:
    """A helper function that helps load data from a supported file to a valid pandas dataframe. If the file is not supported an error is thrown

    Args:
        path (str): The file path to read data from
        config (LoadFileConfigParamType | None, optional): The config to use to customize the loaded data. Defaults to None

    Returns:
        pd.DataFrame: The dataframe loaded from the file
    """

    # Step 1: Check config
    actual_config: LoadFileConfigParamType = {**config} if config else {}
    actual_config_delimiter = actual_config.get("delimiter", ",")
    actual_config_orient = actual_config.get("orient", "records")
    actual_config_dates = actual_config.get("parse_dates", [])

    # Step 2: Load the right file path
    file_extension = check_file_support(path)

    if file_extension == "json":
        return pd.read_json(path, orient=actual_config_orient)
    else:
        return pd.read_csv(
            path,
            parse_dates=actual_config_dates,
            delimiter=actual_config_delimiter,
        )


def write_file(
    path: str, data: pd.DataFrame, config: WriteFileConfigParamType | None = None
):
    """A helper function to help write pandas data to supported files

    Args:
        path (str): The path to the file where the data is formatted to
        data (pd.DataFrame): The data to write as a dataframe
        config (WriteFileConfigParamType | None, optional): The config to use to customize the loaded data. Defaults to None
    """

    # Step 1: Load the actual config
    actual_config: WriteFileConfigParamType = {**config} if config else {}
    actual_config_delimiter = actual_config.get("delimiter", ",")
    actual_config_orient = actual_config.get("orient", "records")

    # Step 2: Write to file
    file_path = check_file_support(path)

    if file_path == "json":
        data.to_json(path, orient=actual_config_orient)
    else:
        data.to_csv(path, sep=actual_config_delimiter)
