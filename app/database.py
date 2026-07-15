from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
import os

# --- PostgreSQL Bağlantısı (Şimdilik İptal) ---
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:sifre123@localhost:5432/transit_yogunluk_db"

# --- SQLite Bağlantısı (Aktif) ---
# Veritabanı dosyası proje ana dizininde "transit_yogunluk.db" adıyla oluşacak
#SQLALCHEMY_DATABASE_URL = "sqlite:///./transit_yogunluk.db"

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres.nuhstqfcyjhxcrsaydio:sifreniz@aws-0-eu-central-1.pooler.supabase.com:6543/postgres")

# SQLite kullanırken aynı thread (iş parçacığı) üzerinden gelen eşzamanlı istekleri yönetebilmek için 
# connect_args={"check_same_thread": False} parametresini eklememiz zorunludur.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()