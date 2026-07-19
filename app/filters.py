from datetime import datetime, timedelta
import uuid
from sqlalchemy.orm import Session
# Yeni oluşturduğumuz AktifYolculuk modelini de dahil ediyoruz
from app.models import YolculukKaydi, Kullanici, Hat, AktifYolculuk


def ortalamayi_etiketle(skor):
    if skor < 4.0:
        return "Rahat"
    elif skor < 7.0:
        return "Orta"
    else:
        return "Yoğun"


def yolculuk_baslat(veri, db: Session):
    su_anki_zaman = datetime.now()
    yolculuk_id = str(uuid.uuid4())

    # Kullanıcının halihazırda devam eden bir yolculuğu var mı kontrolü
    mevcut_yolculuk = db.query(AktifYolculuk).filter(AktifYolculuk.kullanici_id == veri.kullanici_id).first()
    if mevcut_yolculuk:
        return {"hata": "Zaten devam eden aktif bir yolculuğunuz var."}

    # RAM yerine veritabanındaki aktif_yolculuklar tablosuna kaydediyoruz
    yeni_aktif = AktifYolculuk(
        yolculuk_id=yolculuk_id,
        kullanici_id=veri.kullanici_id,
        hat_kodu=veri.hat_kodu,
        binis_duragi=veri.durak_adi,
        baslangic_yogunluk_skoru=veri.yogunluk_skoru,
        binis_zamani=su_anki_zaman
    )

    db.add(yeni_aktif)
    db.commit()

    return {"mesaj": "Yolculuk başlatıldı ve veritabanına kaydedildi.", "yolculuk_id": yolculuk_id}


def yolculuk_bitir(veri, db: Session):
    su_anki_zaman = datetime.now()
    kullanici_id = veri.kullanici_id

    # RAM'den değil, veritabanından başlangıç verisini çekiyoruz
    baslangic_verisi = db.query(AktifYolculuk).filter(AktifYolculuk.kullanici_id == kullanici_id).first()

    if not baslangic_verisi:
        return {"hata": "Aktif bir yolculuğunuz bulunmuyor."}

    gecen_sure = su_anki_zaman - baslangic_verisi.binis_zamani
    dakika_farki = round(gecen_sure.total_seconds() / 60)

    baslangic_skoru = baslangic_verisi.baslangic_yogunluk_skoru
    bitis_skoru = veri.yogunluk_skoru
    temsili_yolculuk_ortalamasi = (baslangic_skoru + bitis_skoru) / 2
    hat_kodu = baslangic_verisi.hat_kodu

    # Yabancı Anahtar (Foreign Key) Kontrolleri
    kullanici_db = db.query(Kullanici).filter(Kullanici.id == kullanici_id).first()
    if not kullanici_db:
        yeni_kullanici = Kullanici(id=kullanici_id)
        db.add(yeni_kullanici)

    hat_db = db.query(Hat).filter(Hat.hat_kodu == hat_kodu).first()
    if not hat_db:
        yeni_hat = Hat(hat_kodu=hat_kodu, aciklama=f"{hat_kodu} Numaralı Hat")
        db.add(yeni_hat)

    # Ana veritabanına kalıcı kayıt oluşturuluyor
    yeni_kayit = YolculukKaydi(
        yolculuk_id=baslangic_verisi.yolculuk_id,
        kullanici_id=kullanici_id,
        hat_kodu=hat_kodu,
        binis_duragi=baslangic_verisi.binis_duragi,
        inis_duragi=veri.durak_adi,
        baslangic_yogunluk_skoru=baslangic_skoru,
        bitis_yogunluk_skoru=bitis_skoru,
        yolculuk_ortalama_skoru=temsili_yolculuk_ortalamasi,
        durum_etiketi=ortalamayi_etiketle(temsili_yolculuk_ortalamasi),
        seyahat_suresi_dk=dakika_farki,
        kayit_zamani=su_anki_zaman
    )

    db.add(yeni_kayit)

    # İşlem tamamlandığı için geçici tablodaki kaydı temizliyoruz
    db.delete(baslangic_verisi)
    db.commit()

    return {
        "mesaj": "Yolculuk başarıyla tamamlandı ve ana kayıtlara işlendi.",
        "yolculuk_id": yeni_kayit.yolculuk_id
    }


def rota_yogunlugu_sorgula(hat_kodu: str, binis_duragi: str, inis_duragi: str, pencere_dk: int, db: Session):
    su_anki_zaman = datetime.now()
    zaman_siniri = su_anki_zaman - timedelta(minutes=pencere_dk)

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