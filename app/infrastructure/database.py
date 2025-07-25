from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import settings

# PostgreSQL connection string format: postgresql://username:password@localhost:5432/dbname
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    pool_size=10,        # Number of connections to keep open in the pool
    max_overflow=20,     # Number of connections to create beyond pool_size when needed
    pool_timeout=30,     # Seconds to wait before giving up on getting a connection
    pool_recycle=1800    # Recycle connections after this many seconds
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for getting DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
