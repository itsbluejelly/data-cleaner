from typing import Literal, List

# The type of files supported in the package
type SupportedFileType = Literal["json", "csv", "text"]

# The files supported in the package
SUPPORTED_FILE_TYPES: List[SupportedFileType] = ["csv", "json", "text"]
