from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path
import uuid

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image, ImageOps, UnidentifiedImageError
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models
from app.auth import aktif_kullanici, parola_dogrula, parola_hashle, token_olustur
from app.database import engine, get_db
from app.filters import rota_yogunlugu_sorgula, yolculuk_baslat, yolculuk_bitir
from app.schemas import KullaniciGiris, KullaniciKayit, YolculukBaslangic, YolculukBitis


PROJE_KOKU = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJE_KOKU / "templates"
UPLOADS_DIR = PROJE_KOKU / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

MAX_FOTOGRAF_BOYUTU = 5 * 1024 * 1024
IZINLI_TURLER = {"image/jpeg", "image/png", "image/webp"}
Image.MAX_IMAGE_PIXELS = 20_000_000

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="RotaRadar API")
app.mount("/static", StaticFiles(directory=TEMPLATES_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.post("/api/auth/kayit", status_code=201)
def kullanici_kayit(veri: KullaniciKayit, db: Session = Depends(get_db)):
    kullanici_adi = veri.kullanici_adi.lower()
    if db.query(models.Kullanici).filter(
        models.Kullanici.kullanici_adi == kullanici_adi
    ).first():
        raise HTTPException(status_code=409, detail="Bu kullanıcı adı zaten alınmış.")

    kullanici = models.Kullanici(
        kullanici_adi=kullanici_adi,
        parola_hash=parola_hashle(veri.parola),
    )
    db.add(kullanici)
    try:
        db.commit()
        db.refresh(kullanici)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Bu kullanıcı adı zaten alınmış.")

    return {
        "access_token": token_olustur(kullanici.id),
        "token_type": "bearer",
        "kullanici_adi": kullanici.kullanici_adi,
    }


@app.post("/api/auth/giris")
def kullanici_giris(veri: KullaniciGiris, db: Session = Depends(get_db)):
    kullanici = db.query(models.Kullanici).filter(
        models.Kullanici.kullanici_adi == veri.kullanici_adi.lower()
    ).first()
    if kullanici is None or not parola_dogrula(veri.parola, kullanici.parola_hash):
        raise HTTPException(status_code=401, detail="Kullanıcı adı veya parola hatalı.")

    return {
        "access_token": token_olustur(kullanici.id),
        "token_type": "bearer",
        "kullanici_adi": kullanici.kullanici_adi,
    }


@app.get("/api/auth/ben")
def ben(kullanici: models.Kullanici = Depends(aktif_kullanici)):
    return {"id": kullanici.id, "kullanici_adi": kullanici.kullanici_adi}


@app.post("/api/yolculuk/basla", status_code=201)
def basla(
    veri: YolculukBaslangic,
    db: Session = Depends(get_db),
    kullanici: models.Kullanici = Depends(aktif_kullanici),
):
    sonuc = yolculuk_baslat(veri, kullanici.id, db)
    if "hata" in sonuc:
        raise HTTPException(status_code=409, detail=sonuc["hata"])
    return sonuc


@app.post("/api/yolculuk/bitir")
def bitir(
    veri: YolculukBitis,
    db: Session = Depends(get_db),
    kullanici: models.Kullanici = Depends(aktif_kullanici),
):
    sonuc = yolculuk_bitir(veri, kullanici.id, db)
    if "hata" in sonuc:
        raise HTTPException(status_code=409, detail=sonuc["hata"])
    return sonuc


@app.get("/api/yolculuk/aktif")
def aktif_yolculuk(
    db: Session = Depends(get_db),
    kullanici: models.Kullanici = Depends(aktif_kullanici),
):
    kayit = db.query(models.AktifYolculuk).filter(
        models.AktifYolculuk.kullanici_id == kullanici.id
    ).first()
    if kayit is None:
        return {"aktif": False}
    return {
        "aktif": True,
        "hat_kodu": kayit.hat_kodu,
        "binis_duragi": kayit.binis_duragi,
    }


@app.get("/api/yogunluk/sorgula")
def yogunluk_sorgula(
    hat_kodu: str,
    binis_duragi: str,
    inis_duragi: str,
    pencere_dk: int = 30,
    db: Session = Depends(get_db),
):
    return rota_yogunlugu_sorgula(
        hat_kodu, binis_duragi, inis_duragi, pencere_dk, db
    )


@app.get("/api/yogunluk/ozet")
def yogunluk_ozeti(db: Session = Depends(get_db)):
    sinir = datetime.now(timezone.utc) - timedelta(minutes=15)
    return db.query(models.YolculukKaydi).filter(
        models.YolculukKaydi.kayit_zamani >= sinir
    ).all()


@app.get("/api/istatistikler/hat-yogunluklari")
def hat_yogunluklari(
    db: Session = Depends(get_db),
    _kullanici: models.Kullanici = Depends(aktif_kullanici),
):
    """Tamamlanmış tüm yolculukların hat bazındaki yoğunluk ortalaması."""
    satirlar = (
        db.query(
            models.YolculukKaydi.hat_kodu,
            func.avg(models.YolculukKaydi.yolculuk_ortalama_skoru),
            func.count(models.YolculukKaydi.yolculuk_id),
        )
        .group_by(models.YolculukKaydi.hat_kodu)
        .order_by(func.avg(models.YolculukKaydi.yolculuk_ortalama_skoru).desc())
        .all()
    )

    return [
        {
            "hat_kodu": hat_kodu,
            "ortalama_yogunluk": round(float(ortalama), 1),
            "yolculuk_sayisi": yolculuk_sayisi,
        }
        for hat_kodu, ortalama, yolculuk_sayisi in satirlar
    ]


@app.post("/api/paylasim", status_code=201)
async def paylasim_olustur(
    hat_kodu: str = Form(..., min_length=1, max_length=20),
    aciklama: str = Form("", max_length=280),
    fotograf: UploadFile = File(...),
    db: Session = Depends(get_db),
    kullanici: models.Kullanici = Depends(aktif_kullanici),
):
    if fotograf.content_type not in IZINLI_TURLER:
        raise HTTPException(status_code=415, detail="Yalnızca JPEG, PNG veya WebP yüklenebilir.")

    icerik = await fotograf.read(MAX_FOTOGRAF_BOYUTU + 1)
    if len(icerik) > MAX_FOTOGRAF_BOYUTU:
        raise HTTPException(status_code=413, detail="Fotoğraf en fazla 5 MB olabilir.")

    try:
        resim = Image.open(BytesIO(icerik))
        resim.verify()
        resim = Image.open(BytesIO(icerik))
        resim = ImageOps.exif_transpose(resim).convert("RGB")
        resim.thumbnail((1600, 1600))
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
        raise HTTPException(status_code=400, detail="Geçerli bir fotoğraf yükleyin.")

    dosya_adi = f"{uuid.uuid4()}.jpg"
    resim.save(UPLOADS_DIR / dosya_adi, "JPEG", quality=85, optimize=True)

    paylasim = models.Paylasim(
        kullanici_id=kullanici.id,
        hat_kodu=hat_kodu.strip().upper(),
        aciklama=aciklama.strip() or None,
        fotograf_yolu=f"/uploads/{dosya_adi}",
    )
    db.add(paylasim)
    db.commit()
    db.refresh(paylasim)
    return {"mesaj": "Paylaşım oluşturuldu.", "id": paylasim.id}


@app.get("/api/paylasimlar")
def paylasimlari_getir(db: Session = Depends(get_db)):
    kayitlar = db.query(models.Paylasim).order_by(
        models.Paylasim.olusturulma_zamani.desc()
    ).limit(50).all()
    return [
        {
            "id": kayit.id,
            "kullanici_adi": kayit.kullanici.kullanici_adi,
            "hat_kodu": kayit.hat_kodu,
            "aciklama": kayit.aciklama,
            "fotograf_url": kayit.fotograf_yolu,
            "olusturulma_zamani": kayit.olusturulma_zamani,
        }
        for kayit in kayitlar
    ]


@app.get("/")
def giris_sayfasi(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@app.get("/uygulama")
def ana_sayfa(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/register")
def kayit_sayfasi(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")
