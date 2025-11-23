from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from src.exceptions.file_exceptions import (
    FolderNotFoundError,
    FileNotFoundError,
    InvalidFileTypeError,
)
from src.core.logger import get_logger

logger = get_logger("FILE_EXCEPTION_HANDLER")


def register_file_error_handlers(app: FastAPI):

    @app.exception_handler(FolderNotFoundError)
    async def folder_not_found_handler(request: Request, exc):
        logger.error(
            "Folder not found: %s. Request URL: %s, Method: %s",
            exc,
            request.url,
            request.method,
        )
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(FileNotFoundError)
    async def file_not_found_handler(request: Request, exc):
        logger.error(
            "File not found: %s. Request URL: %s, Method: %s",
            exc,
            request.url,
            request.method,
        )
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(InvalidFileTypeError)
    async def invalid_file_handler(request: Request, exc):
        logger.error(
            "Invalid file type: %s. Request URL: %s, Method: %s",
            exc,
            request.url,
            request.method,
        )
        return JSONResponse(status_code=400, content={"detail": str(exc)})
