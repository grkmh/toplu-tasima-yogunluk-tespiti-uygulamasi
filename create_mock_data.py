import random
from datetime import datetime, timedelta
import uuid
from app.database import SessionLocal
from app.models import YolculukKaydi, Kullanici, Hat

def create_mock_data():
    db = SessionLocal()
    
    hat_kodu = "622"
    kullanicilar = [f"user_{i}" for i in range(1, 6)]
    
    # Tabloda yoksa Hat ve Kullanıcıları oluştur
    if not db.query(Hat).filter_by(hat_kodu=hat_kodu).first():
        db.add(Hat(hat_kodu=hat_kodu, aciklama="Mock Hat"))
    for k_id in kullanicilar:
        if not db.query(Kullanici).filter_by(id=k_id).first():
            db.add(Kullanici(id=k_id))
    db.commit()

    su_an = datetime.now()
    
    # 50 Adet Normal Veri (3-5 arası puanlar)
    for _ in range(50):
        k_id = random.choice(kullanicilar)
        skor = random.uniform(3.0, 5.0)
        kayit = YolculukKaydi(
            yolculuk_id=str(uuid.uuid4()),
            kullanici_id=k_id,
            hat_kodu=hat_kodu,
            binis_duragi="Durak A",
            inis_duragi="Durak B",
            baslangic_yogunluk_skoru=int(skor),
            bitis_yogunluk_skoru=int(skor)+1,
            yolculuk_ortalama_skoru=skor,
            durum_etiketi="Rahat",
            seyahat_suresi_dk=15,
            kayit_zamani=su_an - timedelta(hours=random.randint(1, 72))
        )
        db.add(kayit)

    # 5 Adet Aykırı Değer / Manipülasyon (Hepsi 9 puan)
    for _ in range(5):
        kayit = YolculukKaydi(
            yolculuk_id=str(uuid.uuid4()),
            kullanici_id=random.choice(kullanicilar),
            hat_kodu=hat_kodu,
            binis_duragi="Durak A",
            inis_duragi="Durak B",
            baslangic_yogunluk_skoru=9,
            bitis_yogunluk_skoru=9,
            yolculuk_ortalama_skoru=9.0,
            durum_etiketi="Yoğun",
            seyahat_suresi_dk=15,
            kayit_zamani=su_an - timedelta(hours=12)
        )
        db.add(kayit)

    db.commit()
    db.close()
    print("Sentetik veriler başarıyla eklendi.")

if __name__ == "__main__":
    create_mock_data()