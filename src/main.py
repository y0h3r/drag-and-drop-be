from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

from src.api.v1 import file, folder

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
)

app.include_router(folder.router, prefix="/api/v1")
app.include_router(file.router, prefix="/api/v1")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # permite estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE...
    allow_headers=["*"],  # cabeceras permitidas
)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}
