from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel  # YENİ EKLENDİ
import sqlite3  # YENİ EKLENDİ

from app.schemas import YolculukBaslangic, YolculukBitis
from app.filters import yolculuk_baslat, yolculuk_bitir, rota_yogunlugu_sorgula
from app.database import engine, get_db
from app import models
from datetime import datetime, timezone
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext


# Bcrypt algoritmasını kullanarak şifreleme bağlamını oluşturuyoruz
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def sifreyi_hashle(parola: str):
    """Kullanıcının girdiği düz şifreyi geri döndürülemez bir hash'e çevirir."""
    return pwd_context.hash(parola)

def sifreyi_dogrula(duz_parola: str, hashli_parola: str):
    """Giriş yaparken girilen şifre ile veritabanındaki hash'in eşleşip eşleşmediğine bakar."""
    return pwd_context.verify(duz_parola, hashli_parola)

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Transit Yoğunluk Takip API")
app.mount("/static", StaticFiles(directory="templates"), name="static")

# Şablonlar için dizin yolu
templates = Jinja2Templates(directory="templates")

# --- YENİ EKLENEN: KULLANICI YÖNETİMİ VERİTABANI ---
def init_auth_db():
    conn = sqlite3.connect("transit.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            soyisim TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_auth_db()


# --- YENİ EKLENEN: KULLANICI PYDANTIC MODELLERİ ---
# --- YENİ KULLANICI DOĞRULAMA MODELLERİ ---
class KullaniciKayit(BaseModel):
    kullanici_adi: str = Field(..., min_length=3, max_length=50)
    parola: str = Field(..., min_length=6)

class KullaniciGiris(BaseModel):
    kullanici_adi: str
    parola: str


class PasswordReset(BaseModel):
    email: str
    new_password: str


# --- YENİ KAYIT VE GİRİŞ API'LERİ ---

@app.post("/api/auth/kayit")
def kullanici_kayit(user: KullaniciKayit):
    # 1. Adım: Kullanıcının girdiği parolayı güvenli bir hash'e dönüştür
    hashed_parola = sifreyi_hashle(user.parola)

    try:
        conn = sqlite3.connect("rotaradar.db")
        cursor = conn.cursor()

        # 2. Adım: Hash'lenmiş parolayı veritabanına kaydet (guven_skoru ve kayit_tarihi otomatik eklenecek)
        cursor.execute("INSERT INTO kullanicilar (kullanici_adi, parola_hash) VALUES (?, ?)",
                       (user.kullanici_adi, hashed_parola))
        conn.commit()
        return {"message": "Kayıt başarıyla oluşturuldu."}

    except sqlite3.IntegrityError:
        # Eğer bu kullanıcı adı (unique constraint) veritabanında varsa hata ver
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten alınmış, lütfen başka bir tane seçin.")
    finally:
        conn.close()


@app.post("/api/auth/giris")
def kullanici_giris(user: KullaniciGiris):
    conn = sqlite3.connect("rotaradar.db")
    cursor = conn.cursor()

    # 1. Adım: Kullanıcı adına göre sistemde böyle biri var mı diye bak
    cursor.execute("SELECT id, parola_hash, kullanici_adi FROM kullanicilar WHERE kullanici_adi=?",
                   (user.kullanici_adi,))
    db_user = cursor.fetchone()
    conn.close()

    # Eğer kayıt bulunamazsa
    if not db_user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")

    # 2. Adım: Formdan gelen açık parolayı, veritabanındaki karmaşık hash (db_user[1]) ile karşılaştır
    if not sifreyi_dogrula(user.parola, db_user[1]):
        raise HTTPException(status_code=401, detail="Hatalı parola girdiniz.")

    # Her şey doğruysa başarılı dönüş yap (ileride buraya JWT oturum anahtarı ekleyeceğiz)
    return {
        "message": "Giriş başarılı",
        "kullanici_id": db_user[0],
        "kullanici_adi": db_user[2]
    }


@app.post("/api/auth/reset-password")
def reset_password(data: PasswordReset):
    if len(data.new_password) < 6:
        raise HTTPException(status_code=400, detail="Yeni şifre en az 6 karakter olmalıdır.")

    conn = sqlite3.connect("transit.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (data.email,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Sistemde böyle bir e-posta adresi bulunamadı.")

    cursor.execute("UPDATE users SET password=? WHERE email=?", (data.new_password, data.email))
    conn.commit()
    conn.close()
    return {"message": "Şifreniz başarıyla yenilendi."}


# MEVCUT API ROTALARI (Dokunulmadı)
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
def yogunluk_sorgula(hat_kodu: str, binis_duragi: str, inis_duragi: str, pencere_dk: int = 30,
                     db: Session = Depends(get_db)):
    return rota_yogunlugu_sorgula(hat_kodu, binis_duragi, inis_duragi, pencere_dk, db)


@app.get("/api/yogunluk/ozet")
def yogunluk_ozeti(db: Session = Depends(get_db)):
    # 1. Şu anki evrensel zamandan 15 dakika öncesini hesapla
    sinir_zaman = datetime.utcnow() - timedelta(minutes=15)

    # 2. Veritabanından son 15 dakikaya ait bitmiş yolculukları çek
    son_15_dk_kayitlari = db.query(models.YolculukKaydi).filter(models.YolculukKaydi.kayit_zamani >= sinir_zaman).all()

    return son_15_dk_kayitlari


# ARAYÜZ ROTALARI
@app.get("/")
def giris_sayfasi(request: Request):
    # Kullanıcı siteye ilk girdiğinde login sayfasını görür
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/uygulama")
def ana_sayfa(request: Request):
    # Giriş yapıldıktan sonra açılacak asıl takip sayfası
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/register")
def kayit_sayfasi(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

@app.get("/reset")
def sifre_yenileme_sayfasi(request: Request):
    return templates.TemplateResponse(request=request, name="reset.html")