from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Yerel SQLite veritabanı dosyamızın yolu
SQLALCHEMY_DATABASE_URL = "sqlite:///./rotaradar.db"

# SQLite, aynı thread (iş parçacığı) üzerinden çalışmayı gerektirdiği için
# check_same_thread ayarını False yapıyoruz.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# main.py'nin aradığı ve API isteklerinde veritabanı bağlantısı sağlayan fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()