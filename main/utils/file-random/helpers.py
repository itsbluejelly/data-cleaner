from schema import SupportedValueType, SUPPORTED_VALUE_TYPES
from faker import Faker
from typing import Dict, TypedDict, NotRequired, List
import random

# A generator for fake data
fake_generator = Faker()


class GenerateFakeValueConfigParamType(TypedDict):
    """A type for the `config` param in the `generate_fake_value` function.

    **NB:** All properties are optional

    Properties:
        1. `decimal_places` (int | None):
        The number of decimal places the random float should have. By default
        its 3.
        **NB:** This is observed only when a `float` value is specified

        2. `min_int` (int | None):
        The minimum inclusive value which the random integer should be based
        off. By default its 0.
        **NB:** This is observed only when a `int` value is specified

        2. `max_int` (int | None):
        The maximum inclusive value which the random integer should be based
        off. By default its 10_000.
        **NB:** This is observed only when a `int` value is specified
    """

    decimal_places: NotRequired[int | None]
    min_int: NotRequired[int | None]
    max_int: NotRequired[int | None]


def generate_fake_headers(
    total_columns: int | None = None,
    default_headers: Dict[str, SupportedValueType] | None = None,
) -> Dict[str, SupportedValueType]:
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
    # Step 1: Properly set config values
    config_total = total_columns or random.randint(1, 5)
    config_headers: Dict[str, SupportedValueType] = (
        {**default_headers} if default_headers else {}
    )

    # Step 2: Limit the headers based on the total
    needed_count = config_total - len(config_headers)

    if needed_count > 0:
        while needed_count != 0:
            # Have a unique key for every pair
            key = fake_generator.word()

            while key in config_headers:
                key = fake_generator.word()

            value = random.choice(SUPPORTED_VALUE_TYPES)

            # Add the value type, and regulate the loop
            config_headers[key] = value
            needed_count -= 1

    return config_headers


def generate_fake_value(
    value_type: SupportedValueType,
    config: GenerateFakeValueConfigParamType | None = None,
):
    """A function that generates a random value based on the type passed in

    Args:
        1. `value_type` (SupportedValueType):
        The type of value to generate, which should be validly supported
        in the app
        2. `config` (GenerateFakeValueConfigParamType, optional):
        The config which controls some aspect of random value generation.

    Returns:
        The random value, which is based on the params given
    """
    # Step 1: Prepare the config object
    actual_config: GenerateFakeValueConfigParamType = {**config} if config else {}
    config_max_int = actual_config.get("max_int") or 10_000
    config_min_int = actual_config.get("min_int") or 0
    config_decimal_places = actual_config.get("decimal_places") or 3

    # Step 2: Generate the values
    if value_type == "boolean":
        return fake_generator.boolean()
    elif value_type == "color":
        return fake_generator.color_name()
    elif value_type == "date":
        return fake_generator.date()
    elif value_type == "email":
        return fake_generator.email()
    elif value_type == "float":
        return round(random.random(), config_decimal_places)
    elif value_type == "int":
        return random.randint(config_min_int, config_max_int)
    elif value_type == "name":
        return fake_generator.name()
    elif value_type == "password":
        return fake_generator.password()
    elif value_type == "string":
        return fake_generator.word()
    elif value_type == "username":
        return fake_generator.user_name()
    else:
        return fake_generator.uuid4()


def generate_fake_rows(
    headers: Dict[str, SupportedValueType],
    default_rows: List[List[int | str | bool | float]] | None = None,
    total_rows: int | None = None,
    value_config: GenerateFakeValueConfigParamType | None = None,
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
        4. `value_config` (GenerateFakeValueConfigParamType | None, optional):
        The config which controls some aspect of random value generation for
        each column in the row.

    Returns:
        A list of all the randomly generated rows, while still abiding by the
        parameters passed in
    """
    # Step 1: Initiate the config and header values
    config_rows = [[*row] for row in default_rows] if default_rows else []
    config_total = total_rows or random.randint(1, 5)

    # Step 2: Ensure the rows are in the required number. Therefore if the
    # rows exceeds the expected number, do nothing as the rows override the
    # count, otherwise add the rest
    needed_count = config_total - len(config_rows)
    header_types = list(headers.values())

    if needed_count > 0:
        new_rows = [
            [
                generate_fake_value(header_type, value_config)
                for header_type in header_types
            ]
            for _ in range(needed_count)
        ]
        config_rows.extend(new_rows)

    return config_rows
