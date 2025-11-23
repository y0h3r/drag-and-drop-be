class BaseAppException(Exception):
    pass


class FolderNotFoundError(BaseAppException):
    pass


class FileNotFoundError(BaseAppException):
    pass


class InvalidFileTypeError(BaseAppException):
    pass
