from typing import Literal, List

# A type for the supported column value in the file
type SupportedValueType = Literal[
    "string",
    "int",
    "float",
    "boolean",
    "date",
    "name",
    "email",
    "password",
    "username",
    "color",
    "uuid",
]

# A value that holds all the constants for the types of column values
# supported in the application
SUPPORTED_VALUE_TYPES: List[SupportedValueType] = [
    "boolean",
    "color",
    "date",
    "email",
    "float",
    "int",
    "name",
    "password",
    "string",
    "username",
    "uuid",
]
