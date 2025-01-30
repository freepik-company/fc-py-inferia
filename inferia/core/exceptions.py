from os import PathLike


class ConfigFileNotFoundError(Exception):
    def __init__(self, file_path: str):
        super().__init__(f"Config file not found: {file_path}")


class SetupError(Exception):
    def __init__(self, predictor: str, error: Exception):
        super().__init__(f"Unable to setup predictor {predictor}: {error}")


class InvalidHandlerSignature(Exception):
    def __init__(self, class_name: str):
        super().__init__(class_name)


class NoThreadsAvailableError(Exception):
    def __init__(self, class_name: str):
        super().__init__(f"No threads available for {class_name}")
