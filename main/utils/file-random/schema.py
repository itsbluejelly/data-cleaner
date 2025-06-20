from typing import Literal, List

# A type for the supported column value in the csv file
type SupportedValueType = Literal[
    "string",
    "int",
    "float",
    "boolean",
    "date",
    "track",
    "name",
    "email",
    "password",
    "username",
    "color",
    "uuid",
]

# A value that holds all the constants for the types of column values
# supported in the application
SUPPORTED_TYPES: List[SupportedValueType] = [
    "boolean",
    "color",
    "date",
    "email",
    "float",
    "int",
    "name",
    "password",
    "string",
    "track",
    "username",
    "uuid",
]
