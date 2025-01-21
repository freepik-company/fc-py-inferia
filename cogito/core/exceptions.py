from os import PathLike


class ConfigFileNotFoundError(Exception):
    def __init__(self, file_path: str):
        super().__init__(f"Config file not found: {file_path}")

class InvalidHandlerSignature(Exception):
    def __init__(self, class_name: str):
        super().__init__(class_name)
