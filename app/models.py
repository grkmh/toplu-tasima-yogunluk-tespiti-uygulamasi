from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


def utc_now():
    return datetime.now(timezone.utc)


class Kullanici(Base):
    __tablename__ = "kullanicilar"

    id = Column(Integer, primary_key=True, index=True)
    kullanici_adi = Column(String(50), unique=True, index=True, nullable=False)
    parola_hash = Column(String(255), nullable=False)
    guven_skoru = Column(Integer, default=100, nullable=False)
    kayit_tarihi = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    yolculuklar = relationship("YolculukKaydi", back_populates="kullanici")
    aktif_yolculuk = relationship("AktifYolculuk", back_populates="kullanici", uselist=False)
    paylasimlar = relationship("Paylasim", back_populates="kullanici")


class Hat(Base):
    __tablename__ = "hatlar"

    hat_kodu = Column(String(20), primary_key=True, index=True)
    aciklama = Column(String(200), nullable=True)

    yolculuklar = relationship("YolculukKaydi", back_populates="hat")


class YolculukKaydi(Base):
    __tablename__ = "yolculuk_kayitlari"

    yolculuk_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    kullanici_id = Column(Integer, ForeignKey("kullanicilar.id"), nullable=False, index=True)
    hat_kodu = Column(String(20), ForeignKey("hatlar.hat_kodu"), nullable=False)
    binis_duragi = Column(String(100), nullable=False)
    inis_duragi = Column(String(100), nullable=False)
    baslangic_yogunluk_skoru = Column(Integer, nullable=False)
    bitis_yogunluk_skoru = Column(Integer, nullable=False)
    yolculuk_ortalama_skoru = Column(Float, nullable=False)
    durum_etiketi = Column(String(20), nullable=False)
    seyahat_suresi_dk = Column(Integer, nullable=False)
    kayit_zamani = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    kullanici = relationship("Kullanici", back_populates="yolculuklar")
    hat = relationship("Hat", back_populates="yolculuklar")


class GunlukOzet(Base):
    __tablename__ = "gunluk_ozetler"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hat_kodu = Column(String(20), index=True)
    binis_duragi = Column(String(100))
    inis_duragi = Column(String(100))
    temiz_ortalama = Column(Float, nullable=False)
    toplam_veri_sayisi = Column(Integer, nullable=False)
    aykiri_veri_sayisi = Column(Integer, nullable=False)
    analiz_tarihi = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class AktifYolculuk(Base):
    __tablename__ = "aktif_yolculuklar"

    yolculuk_id = Column(String, primary_key=True)
    kullanici_id = Column(
        Integer,
        ForeignKey("kullanicilar.id"),
        unique=True,
        nullable=False,
        index=True,
    )
    hat_kodu = Column(String(20), ForeignKey("hatlar.hat_kodu"), nullable=False)
    binis_duragi = Column(String(100), nullable=False)
    baslangic_yogunluk_skoru = Column(Integer, nullable=False)
    binis_zamani = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    kullanici = relationship("Kullanici", back_populates="aktif_yolculuk")


class Paylasim(Base):
    __tablename__ = "paylasimlar"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    kullanici_id = Column(Integer, ForeignKey("kullanicilar.id"), nullable=False, index=True)
    hat_kodu = Column(String(20), nullable=False, index=True)
    aciklama = Column(String(280), nullable=True)
    fotograf_yolu = Column(String(255), nullable=False)
    olusturulma_zamani = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    kullanici = relationship("Kullanici", back_populates="paylasimlar")
