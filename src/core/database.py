from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import ssl
from src.core.config import settings

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE  # Cambia según tu setup

engine = create_async_engine(
    settings.DATABASE_URL,
    connect_args={"ssl": ssl_context},  # <- aquí evitamos sslmode en URL
    future=True,
    echo=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
