from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.exceptions.folder_exceptions import (
    FolderNotFoundError,
    InvalidFolderParentError,
    UnexpectedFolderError,
)
from src.core.logger import get_logger

logger = get_logger("FOLDER_EXCEPTION_HANDLER")


def register_folder_exception_handlers(app: FastAPI):

    @app.exception_handler(FolderNotFoundError)
    async def folder_not_found_handler(request: Request, exc: FolderNotFoundError):
        logger.error(
            "Folder not found: %s. Request URL: %s, Method: %s",
            exc,
            request.url,
            request.method,
        )
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc) or "Folder not found"},
        )

    @app.exception_handler(UnexpectedFolderError)
    async def unexpected_folder_error_handler(
        request: Request, exc: UnexpectedFolderError
    ):
        logger.exception(
            "Unexpected folder error: %s. Request URL: %s, Method: %s",
            exc,
            request.url,
            request.method,
        )
        return JSONResponse(
            status_code=500,
            content={
                "detail": "An unexpected error occurred while processing the folder."
            },
        )

    @app.exception_handler(InvalidFolderParentError)
    async def invalid_folder_parent_handler(
        request: Request, exc: InvalidFolderParentError
    ):
        logger.error(
            "Invalid folder parent: %s. Request URL: %s, Method: %s",
            exc,
            request.url,
            request.method,
        )
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc) or "Invalid parent folder"},
        )
