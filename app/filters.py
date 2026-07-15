from datetime import datetime, timedelta
import uuid
from sqlalchemy.orm import Session
from app.models import YolculukKaydi, Kullanici, Hat

# Aktif (henüz bitmemiş) yolculukları geçici olarak RAM'de tutuyoruz.
aktif_yolculuklar = {}

def ortalamayi_etiketle(skor):
    if skor < 4.0:
        return "Rahat"
    elif skor < 7.0:
        return "Orta"
    else:
        return "Yoğun"

def yolculuk_baslat(veri):
    su_anki_zaman = datetime.now()
    yolculuk_id = str(uuid.uuid4())
    
    aktif_yolculuklar[veri.kullanici_id] = {
        "yolculuk_id": yolculuk_id,
        "hat_kodu": veri.hat_kodu,
        "binis_duragi": veri.durak_adi,
        "baslangic_yogunluk_skoru": veri.yogunluk_skoru,
        "binis_zamani": su_anki_zaman
    }
    return {"mesaj": "Yolculuk başlatıldı.", "yolculuk_id": yolculuk_id}

def yolculuk_bitir(veri, db: Session):
    su_anki_zaman = datetime.now()
    kullanici_id = veri.kullanici_id
    
    if kullanici_id not in aktif_yolculuklar:
        return {"hata": "Aktif bir yolculuğunuz bulunmuyor."}
        
    baslangic_verisi = aktif_yolculuklar[kullanici_id]
    gecen_sure = su_anki_zaman - baslangic_verisi["binis_zamani"]
    dakika_farki = round(gecen_sure.total_seconds() / 60)
    
    baslangic_skoru = baslangic_verisi["baslangic_yogunluk_skoru"]
    bitis_skoru = veri.yogunluk_skoru
    temsili_yolculuk_ortalamasi = (baslangic_skoru + bitis_skoru) / 2
    hat_kodu = baslangic_verisi["hat_kodu"]

    # --- Yabancı Anahtar (Foreign Key) Kontrolleri ---
    # Kullanıcı tabloda yoksa test amaçlı otomatik oluştur
    kullanici_db = db.query(Kullanici).filter(Kullanici.id == kullanici_id).first()
    if not kullanici_db:
        yeni_kullanici = Kullanici(id=kullanici_id)
        db.add(yeni_kullanici)

    # Hat tabloda yoksa test amaçlı otomatik oluştur
    hat_db = db.query(Hat).filter(Hat.hat_kodu == hat_kodu).first()
    if not hat_db:
        yeni_hat = Hat(hat_kodu=hat_kodu, aciklama=f"{hat_kodu} Numaralı Hat")
        db.add(yeni_hat)
    
    # --- SQLAlchemy ile Veritabanına Kayıt ---
    yeni_kayit = YolculukKaydi(
        yolculuk_id=baslangic_verisi["yolculuk_id"],
        kullanici_id=kullanici_id,
        hat_kodu=hat_kodu,
        binis_duragi=baslangic_verisi["binis_duragi"],
        inis_duragi=veri.durak_adi,
        baslangic_yogunluk_skoru=baslangic_skoru,
        bitis_yogunluk_skoru=bitis_skoru,
        yolculuk_ortalama_skoru=temsili_yolculuk_ortalamasi,
        durum_etiketi=ortalamayi_etiketle(temsili_yolculuk_ortalamasi),
        seyahat_suresi_dk=dakika_farki,
        kayit_zamani=su_anki_zaman
    )
    
    db.add(yeni_kayit)
    db.commit() 
    
    del aktif_yolculuklar[kullanici_id]
    
    return {
        "mesaj": "Yolculuk başarıyla veritabanına kaydedildi.",
        "yolculuk_id": yeni_kayit.yolculuk_id
    }

def rota_yogunlugu_sorgula(hat_kodu: str, binis_duragi: str, inis_duragi: str, pencere_dk: int, db: Session):
    su_anki_zaman = datetime.now()
    zaman_siniri = su_anki_zaman - timedelta(minutes=pencere_dk)
    
    # Veritabanından geçmiş kayıtlara göre filtreleme yapıyoruz
    kayitlar = db.query(YolculukKaydi).filter(
        YolculukKaydi.hat_kodu == hat_kodu,
        YolculukKaydi.binis_duragi == binis_duragi,
        YolculukKaydi.inis_duragi == inis_duragi,
        YolculukKaydi.kayit_zamani >= zaman_siniri
    ).all()
    
    if not kayitlar:
        return {
            "hat_kodu": hat_kodu,
            "binis_duragi": binis_duragi,
            "inis_duragi": inis_duragi,
            "guncel_ortalama_skor": None,
            "durum_etiketi": "Veri Yok",
            "aktif_veri_sayisi": 0
        }
        
    toplam_skor = sum([k.yolculuk_ortalama_skoru for k in kayitlar])
    genel_hat_ortalamasi = toplam_skor / len(kayitlar)
    
    return {
        "hat_kodu": hat_kodu,
        "binis_duragi": binis_duragi,
        "inis_duragi": inis_duragi,
        "guncel_ortalama_skor": round(genel_hat_ortalamasi, 1),
        "durum_etiketi": ortalamayi_etiketle(genel_hat_ortalamasi),
        "aktif_veri_sayisi": len(kayitlar)
    }