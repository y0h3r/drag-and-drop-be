class FolderError(Exception):
    pass


class FolderNotFoundError(FolderError):
    pass


class UnexpectedFolderError(FolderError):
    pass


class InvalidFolderParentError(FolderError):
    pass
