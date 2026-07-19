from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.schemas import YolculukBaslangic, YolculukBitis
from app.filters import yolculuk_baslat, yolculuk_bitir, rota_yogunlugu_sorgula
from app.database import engine, get_db
from app import models
from datetime import datetime, timedelta

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Transit Yoğunluk Takip API")

# Şablonlar için dizin yolu
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ARAYÜZ ROTASI
@app.get("/")
def ana_sayfa(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# API ROTALARI
@app.post("/api/yolculuk/basla")
def basla(veri: YolculukBaslangic, db: Session = Depends(get_db)):
    return yolculuk_baslat(veri, db)

@app.post("/api/yolculuk/bitir")
def bitir(veri: YolculukBitis, db: Session = Depends(get_db)):
    sonuc = yolculuk_bitir(veri, db)
    if "hata" in sonuc:
        raise HTTPException(status_code=400, detail=sonuc["hata"])
    return sonuc

@app.get("/api/yogunluk/sorgula")
def yogunluk_sorgula(hat_kodu: str, binis_duragi: str, inis_duragi: str, pencere_dk: int = 30, db: Session = Depends(get_db)):
    return rota_yogunlugu_sorgula(hat_kodu, binis_duragi, inis_duragi, pencere_dk, db)


@app.get("/api/yogunluk/ozet")
def yogunluk_ozeti(db: Session = Depends(get_db)):
    # 1. Şu anki evrensel zamandan 15 dakika öncesini hesapla
    sinir_zaman = datetime.utcnow() - timedelta(minutes=15)

    # 2. Veritabanından son 15 dakikaya ait bitmiş yolculukları çek
    son_15_dk_kayitlari = db.query(models.YolculukKaydi).filter(models.YolculukKaydi.kayit_zamani >= sinir_zaman).all()

    return son_15_dk_kayitlari