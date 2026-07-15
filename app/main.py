from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.schemas import YolculukBaslangic, YolculukBitis
from app.filters import yolculuk_baslat, yolculuk_bitir, rota_yogunlugu_sorgula
from app.database import engine, get_db
from app import models

# Bu satır, uygulama başladığında veritabanı tablolarını otomatik oluşturur
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Transit Yoğunluk Takip API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/yolculuk/basla")
def basla(veri: YolculukBaslangic, db: Session = Depends(get_db)):
    # db objesi içeri aktarıldı, filters.py güncellendiğinde bu objeyi kullanacağız
    return yolculuk_baslat(veri)

@app.post("/api/yolculuk/bitir")
def bitir(veri: YolculukBitis, db: Session = Depends(get_db)):
    sonuc = yolculuk_bitir(veri, db)
    if "hata" in sonuc:
        raise HTTPException(status_code=400, detail=sonuc["hata"])
    return sonuc

@app.get("/api/yogunluk/sorgula")
def yogunluk_sorgula(hat_kodu: str, binis_duragi: str, inis_duragi: str, pencere_dk: int = 30, db: Session = Depends(get_db)):
    # db parametresini filters.py'deki fonksiyona iletiyoruz
    return rota_yogunlugu_sorgula(hat_kodu, binis_duragi, inis_duragi, pencere_dk, db)

@app.get("/api/yogunluk/ozet")
def gunluk_ozet_getir(db: Session = Depends(get_db)):
    # Veritabanından en güncel temizlenmiş özet verilerini çekiyoruz.
    # analiz_tarihi'ne göre azalan (desc) sıralama yaparak en yeni verilerin üstte gelmesini sağlıyoruz.
    ozetler = db.query(models.GunlukOzet).order_by(models.GunlukOzet.analiz_tarihi.desc()).limit(100).all()
    
    if not ozetler:
        return {"mesaj": "Henüz gün sonu temizlik verisi oluşmadı veya veritabanı boş."}
        
    return ozetler