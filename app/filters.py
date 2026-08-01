from datetime import datetime, timedelta, timezone
import uuid

from sqlalchemy.orm import Session

from app.models import AktifYolculuk, Hat, YolculukKaydi


def utc_now():
    return datetime.now(timezone.utc)


def ortalamayi_etiketle(skor):
    if skor < 4.0:
        return "Rahat"
    if skor < 7.0:
        return "Orta"
    return "Yoğun"


def yolculuk_baslat(veri, kullanici_id: int, db: Session):
    mevcut = db.query(AktifYolculuk).filter(
        AktifYolculuk.kullanici_id == kullanici_id
    ).first()
    if mevcut:
        return {"hata": "Zaten devam eden aktif bir yolculuğunuz var."}

    hat = db.query(Hat).filter(Hat.hat_kodu == veri.hat_kodu).first()
    if hat is None:
        db.add(Hat(hat_kodu=veri.hat_kodu, aciklama=f"{veri.hat_kodu} Numaralı Hat"))
        db.flush()

    yolculuk_id = str(uuid.uuid4())
    db.add(AktifYolculuk(
        yolculuk_id=yolculuk_id,
        kullanici_id=kullanici_id,
        hat_kodu=veri.hat_kodu,
        binis_duragi=veri.durak_adi,
        baslangic_yogunluk_skoru=veri.yogunluk_skoru,
        binis_zamani=utc_now(),
    ))
    db.commit()
    return {"mesaj": "Yolculuk başlatıldı.", "yolculuk_id": yolculuk_id}


def yolculuk_bitir(veri, kullanici_id: int, db: Session):
    baslangic = db.query(AktifYolculuk).filter(
        AktifYolculuk.kullanici_id == kullanici_id
    ).first()
    if baslangic is None:
        return {"hata": "Aktif bir yolculuğunuz bulunmuyor."}

    simdi = utc_now()
    binis = baslangic.binis_zamani
    if binis.tzinfo is None:
        binis = binis.replace(tzinfo=timezone.utc)

    sure = max(0, round((simdi - binis).total_seconds() / 60))
    ortalama = (baslangic.baslangic_yogunluk_skoru + veri.yogunluk_skoru) / 2

    db.add(YolculukKaydi(
        yolculuk_id=baslangic.yolculuk_id,
        kullanici_id=kullanici_id,
        hat_kodu=baslangic.hat_kodu,
        binis_duragi=baslangic.binis_duragi,
        inis_duragi=veri.durak_adi,
        baslangic_yogunluk_skoru=baslangic.baslangic_yogunluk_skoru,
        bitis_yogunluk_skoru=veri.yogunluk_skoru,
        yolculuk_ortalama_skoru=ortalama,
        durum_etiketi=ortalamayi_etiketle(ortalama),
        seyahat_suresi_dk=sure,
        kayit_zamani=simdi,
    ))
    db.delete(baslangic)
    db.commit()
    return {"mesaj": "Yolculuk başarıyla tamamlandı."}


def rota_yogunlugu_sorgula(hat_kodu, binis_duragi, inis_duragi, pencere_dk, db):
    zaman_siniri = utc_now() - timedelta(minutes=pencere_dk)
    kayitlar = db.query(YolculukKaydi).filter(
        YolculukKaydi.hat_kodu == hat_kodu,
        YolculukKaydi.binis_duragi == binis_duragi,
        YolculukKaydi.inis_duragi == inis_duragi,
        YolculukKaydi.kayit_zamani >= zaman_siniri,
    ).all()

    if not kayitlar:
        return {
            "hat_kodu": hat_kodu,
            "binis_duragi": binis_duragi,
            "inis_duragi": inis_duragi,
            "guncel_ortalama_skor": None,
            "durum_etiketi": "Veri Yok",
            "aktif_veri_sayisi": 0,
        }

    ortalama = sum(k.yolculuk_ortalama_skoru for k in kayitlar) / len(kayitlar)
    return {
        "hat_kodu": hat_kodu,
        "binis_duragi": binis_duragi,
        "inis_duragi": inis_duragi,
        "guncel_ortalama_skor": round(ortalama, 1),
        "durum_etiketi": ortalamayi_etiketle(ortalama),
        "aktif_veri_sayisi": len(kayitlar),
    }
