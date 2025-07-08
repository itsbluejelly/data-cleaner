from main.utils.file_loader.helpers import (
    write_file,
    WriteFileConfigParamType as OGWriteFileConfigParamType,
)
import pandas as pd
from typing import TypedDict, NotRequired, Literal


class WriteFileConfigParamType(TypedDict):
    """A type for the `config` param in the `write_file` loader file helper function.

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


class DataClass:
    # Default configs
    DEFAULT_WRITE_FILE_PARAM_CONFIG: OGWriteFileConfigParamType = {
        "delimiter": ",",
        "orient": "records",
    }

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def write_file(self, path: str, config: WriteFileConfigParamType | None = None):
        """A function to help write pandas data to supported files

        Args:
            path (str): The path to the file where the data is formatted to
            config (WriteFileConfigParamType | None, optional): The config to use to customize the loaded data. Defaults to `DEFAULT_WRITE_FILE_PARAM_CONFIG`.
        """

        default_config: OGWriteFileConfigParamType = {
            **self.DEFAULT_WRITE_FILE_PARAM_CONFIG,
            **(config or {}),
        }

        return write_file(path, self.data, default_config)

