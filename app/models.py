from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base = declarative_base()

class Kullanici(Base):
    __tablename__ = "kullanicilar"

    id = Column(String, primary_key=True, index=True)
    guven_skoru = Column(Float, default=1.0)
    kayit_tarihi = Column(DateTime, default=datetime.utcnow)

    yolculuklar = relationship("YolculukKaydi", back_populates="kullanici")

class Hat(Base):
    __tablename__ = "hatlar"

    hat_kodu = Column(String, primary_key=True, index=True)
    aciklama = Column(String, nullable=True)

    yolculuklar = relationship("YolculukKaydi", back_populates="hat")

class YolculukKaydi(Base):
    __tablename__ = "yolculuk_kayitlari"

    yolculuk_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    kullanici_id = Column(String, ForeignKey("kullanicilar.id"))
    hat_kodu = Column(String, ForeignKey("hatlar.hat_kodu"))

    binis_duragi = Column(String, nullable=False)
    inis_duragi = Column(String, nullable=False)

    baslangic_yogunluk_skoru = Column(Integer, nullable=False)
    bitis_yogunluk_skoru = Column(Integer, nullable=False)
    yolculuk_ortalama_skoru = Column(Float, nullable=False)
    
    durum_etiketi = Column(String, nullable=False)
    seyahat_suresi_dk = Column(Integer, nullable=False)
    
    kayit_zamani = Column(DateTime, default=datetime.utcnow)

    kullanici = relationship("Kullanici", back_populates="yolculuklar")
    hat = relationship("Hat", back_populates="yolculuklar")

class GunlukOzet(Base):
    __tablename__ = "gunluk_ozetler"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hat_kodu = Column(String, index=True)
    binis_duragi = Column(String)
    inis_duragi = Column(String)
    
    temiz_ortalama = Column(Float, nullable=False)
    toplam_veri_sayisi = Column(Integer, nullable=False)
    aykiri_veri_sayisi = Column(Integer, nullable=False)
    
    analiz_tarihi = Column(DateTime, default=datetime.utcnow)