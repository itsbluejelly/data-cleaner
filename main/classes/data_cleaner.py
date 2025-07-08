from main.utils.file_random.helpers import (
    generate_fake_headers,
    generate_fake_value,
    generate_fake_rows,
    ConfigType as OGFileRandomConfigType,
)
from main.utils.file_random.schema import SupportedValueType
import random
from typing import Dict, NotRequired, TypedDict, List, Sequence, Mapping, Literal
from main.utils.file_loader.helpers import (
    load_file,
    LoadFileConfigParamType as OGLoadFileConfigParamType,
)
from .data_class import DataClass


class FileRandomConfigType(TypedDict):
    """A type for the `config` param in the helper random file functions.

    **NB:** All properties are optional

    Properties:
        1. `decimal_places` (int):
        The number of decimal places the random float should have. By default
        its 3.

        2. `min_int` (int):
        The minimum inclusive value which the random integer should be based
        off. By default its 0.

        2. `max_int` (int):
        The maximum inclusive value which the random integer should be based
        off. By default its 10_000.
    """

    decimal_places: NotRequired[int]
    min_int: NotRequired[int]
    max_int: NotRequired[int]


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


class DataCleaner:
    # Default configs
    DEFAULT_FILE_RANDOM_CONFIG: OGFileRandomConfigType = {
        "decimal_places": 3,
        "max_int": 10_000,
        "min_int": 0,
    }

    DEFAULT_LOAD_FILE_PARAM_CONFIG: OGLoadFileConfigParamType = {
        "delimiter": ",",
        "orient": "records",
        "parse_dates": [],
    }

    @staticmethod
    def generate_fake_headers(
        total_columns: int | None = None,
        default_headers: Dict[str, SupportedValueType] | None = None,
    ):
        """A function that generates random headers, based on the total
        parameter, while still prioritising the default headers passed in

        Args:
            1. `total_columns` (int | None, optional):
            _description_. A value that determines how many header columns are
            generated randomly. By default, it's any number between 1-5 inclusive

            2. `default_headers` (Dict[str, SupportedValueType] | None, optional):
            _description_. A dict that contains the default key-value pairs, with
            the key as the header title, and the column type for that header. If
            the number of pairs exceeds the total specified, then the headers are
            prioritised hence we get the headers passed in. By default, it's an
            empty object

        Returns:
            An object containing the random header titles and their column types,
            as per the config params passed in
        """
        # Declare defaults
        actual_headers: Dict[str, SupportedValueType] = (
            {**default_headers} if default_headers else {}
        )

        default_total = total_columns or random.randint(0, 5)

        return generate_fake_headers(default_total, actual_headers)

    @classmethod
    def get_file_random_config(
        cls,
        config: FileRandomConfigType | None = None,
    ) -> OGFileRandomConfigType:
        """A function to convert an optional config an prepare defaults for missing properties. If the whole config's properties are given then it returns it as is, effectively preserving it

        Args:
            config (FileRandomConfigType | None, optional):
            The optional config to work with. Defaults to the default config values.

        Returns:
            The config with resolved properties
        """
        return {**cls.DEFAULT_FILE_RANDOM_CONFIG, **(config or {})}

    @classmethod
    def generate_fake_value(
        cls,
        value_type: SupportedValueType,
        config: FileRandomConfigType | None = None,
    ):
        """A function that generates a random value based on the type passed in

        Args:
            1. `value_type` (SupportedValueType):
                The type of value to generate, which should be validly supported
                in the app
            2. `config` (FileRandomConfigType | None, optional):
                The config which controls some aspect of random value generation. Defaults to `DEFAULT_FILE_RANDOM_CONFIG`.

        Returns:
            The random value, which is based on the params given
        """
        return generate_fake_value(value_type, cls.get_file_random_config(config))

    @classmethod
    def generate_fake_rows(
        cls,
        headers: Dict[str, SupportedValueType],
        default_rows: List[List[int | str | bool | float]] | None = None,
        total_rows: int | None = None,
        value_config: FileRandomConfigType | None = None,
    ):
        """A function that generates random rows of data, based on the total_rows
        parameter count, while still preserving the default rows passed in. It
        also ensures the number of columns are kept in accordance to the header
        structure provided

        Args:
            1. `headers` (Dict[str, SupportedValueType]):
            The headers to use in the random row generation, which consists of the
            header name and its type for each key-value pair. The number of pairs
            determines the number of columns in each row
            2. `rows` (List[List[int  |  str  |  bool  |  float]] | None, optional)
            A list of the default rows to include in the random rows generation,
            with each row consisting of default column values. Defaults to an
            empty list.
            3. `total_rows` (int | None, optional):
            The total number of rows to randomly generate. Defaults to a number
            between 1-5 inclusive
            4. `value_config` (ConfigType | None, optional):
            The config which controls some aspect of random value generation for
            each column in the row. Defaults to `DEFAULT_FILE_RANDOM_CONFIG`

        Returns:
            A list of all the randomly generated rows, while still abiding by the
            parameters passed in
        """
        # Declare defaults
        config_rows = [[*row] for row in default_rows] if default_rows else []
        default_total = total_rows or random.randint(1, 5)

        return generate_fake_rows(
            headers,
            config_rows,
            default_total,
            cls.get_file_random_config(value_config),
        )

    @classmethod
    def load_file(
        cls, path: str, config: LoadFileConfigParamType | None = None
    ) -> DataClass:
        """A function that helps load data from a supported file to a data class instance.

        Args:
            path (str): The file path to read data from
            config (LoadFileConfigParamType | None, optional): The config to use to customize the loaded data. Defaults to `DEFAULT_LOAD_FILE_PARAM_CONFIG`.

        Returns:
            DataClass: The data class instance, with all data-level APIs and properties
        """
        default_config: OGLoadFileConfigParamType = {
            **cls.DEFAULT_LOAD_FILE_PARAM_CONFIG,
            **(config or {}),
        }

        data = load_file(path, default_config)

        return DataClass(data)

data_cleaner = DataCleaner()