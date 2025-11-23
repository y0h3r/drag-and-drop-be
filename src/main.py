from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import folder_router
from src.api.v1 import file_router
from src.exceptions.file_exception_handler import register_file_error_handlers
from src.exceptions.folder_exception_handler import register_folder_exception_handlers
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
)

register_folder_exception_handlers(app)
register_file_error_handlers(app)

app.include_router(folder_router.router, prefix="/api/v1")
app.include_router(file_router.router, prefix="/api/v1")

origins = [
    "http://localhost:5173",
]

isDevEnv = settings.ENV is "DEV"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if isDevEnv else "*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}
