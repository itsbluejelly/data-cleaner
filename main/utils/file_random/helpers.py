from .schema import SupportedValueType, SUPPORTED_VALUE_TYPES
from faker import Faker
from typing import Dict, TypedDict, List
import random

# A generator for fake data
fake_generator = Faker()


class ConfigType(TypedDict):
    """A type for the `config` param in the generator functions.

    Properties:
        1. `decimal_places` (int):
        The number of decimal places the random float should have.

        2. `min_int` (int):
        The minimum inclusive value which the random integer should be based
        off.

        2. `max_int` (int):
        The maximum inclusive value which the random integer should be based
        off.
    """
    decimal_places: int
    min_int: int
    max_int: int


def generate_fake_headers(
    total_columns: int,
    default_headers: Dict[str, SupportedValueType],
) -> Dict[str, SupportedValueType]:
    """A function that generates random headers, based on the total
    parameter, while still prioritising the default headers passed in

    Args:
        1. `total_columns` (int ):
        _description_. A value that determines how many header columns are
        generated randomly.

        2. `default_headers` (Dict[str, SupportedValueType]):
        _description_. A dict that contains the default key-value pairs, with
        the key as the header title, and the column type for that header. If
        the number of pairs exceeds the total specified, then the headers are
        prioritised hence we get the headers passed in.

    Returns:
        An object containing the random header titles and their column types,
        as per the config params passed in
    """
    needed_count = total_columns - len(default_headers)

    if needed_count > 0:
        while needed_count != 0:
            # Have a unique key for every pair
            key = fake_generator.word()

            while key in default_headers:
                key = fake_generator.word()

            value = random.choice(SUPPORTED_VALUE_TYPES)

            # Add the value type, and regulate the loop
            default_headers[key] = value
            needed_count -= 1

    return default_headers


def generate_fake_value(
    value_type: SupportedValueType,
    config: ConfigType,
):
    """A function that generates a random value based on the type passed in

    Args:
        1. `value_type` (SupportedValueType):
        The type of value to generate, which should be validly supported
        in the app
        2. `config` (ConfigType):
        The config which controls some aspect of random value generation.

    Returns:
        The random value, which is based on the params given
    """
    if value_type == "boolean":
        return fake_generator.boolean()
    elif value_type == "color":
        return fake_generator.color_name()
    elif value_type == "date":
        return fake_generator.date()
    elif value_type == "email":
        return fake_generator.email()
    elif value_type == "float":
        return round(random.random(), config["decimal_places"])
    elif value_type == "int":
        return random.randint(config["min_int"], config["max_int"])
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
    default_rows: List[List[int | str | bool | float]],
    total_rows: int,
    value_config: ConfigType,
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
        2. `rows` (List[List[int  |  str  |  bool  |  float]])
        A list of the default rows to include in the random rows generation,
        with each row consisting of default column values.
        3. `total_rows` (int):
        The total number of rows to randomly generate.
        4. `value_config` (ConfigType):
        The config which controls some aspect of random value generation for
        each column in the row.

    Returns:
        A list of all the randomly generated rows, while still abiding by the
        parameters passed in
    """
    needed_count = total_rows - len(default_rows)
    header_types = list(headers.values())

    if needed_count > 0:
        new_rows = [
            [
                generate_fake_value(header_type, value_config)
                for header_type in header_types
            ]
            for _ in range(needed_count)
        ]
        default_rows.extend(new_rows)

    return default_rows
