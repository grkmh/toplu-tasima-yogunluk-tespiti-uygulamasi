import pandas as pd
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import GunlukOzet

def gun_sonu_analizi_ve_temizlik():
    # 1. Veriyi Veritabanından Pandas DataFrame'ine Çek
    sorgu = "SELECT * FROM yolculuk_kayitlari"
    df = pd.read_sql(sorgu, engine)

    if df.empty:
        print("İşlenecek veri bulunamadı.")
        return

    segment_gruplari = df.groupby(['hat_kodu', 'binis_duragi', 'inis_duragi'])
    temizlenmis_veriler = []
    
    # Veritabanı oturumunu aç
    db = SessionLocal()

    for isim, grup in segment_gruplari:
        # IQR Algoritması
        Q1 = grup['yolculuk_ortalama_skoru'].quantile(0.25)
        Q3 = grup['yolculuk_ortalama_skoru'].quantile(0.75)
        IQR = Q3 - Q1

        alt_sinir = Q1 - 1.5 * IQR
        ust_sinir = Q3 + 1.5 * IQR

        # Temizlenmiş veri seti (Sınırlar içindeki veriler)
        temiz_grup = grup[(grup['yolculuk_ortalama_skoru'] >= alt_sinir) & 
                          (grup['yolculuk_ortalama_skoru'] <= ust_sinir)]
        
        temiz_ortalama = temiz_grup['yolculuk_ortalama_skoru'].mean()
        ham_ortalama = grup['yolculuk_ortalama_skoru'].mean()
        
        toplam_veri = len(grup)
        aykiri_veri = toplam_veri - len(temiz_grup)

        # Ekrana basmak için listeye ekle
        temizlenmis_veriler.append({
            'Hat Kodu': isim[0],
            'Biniş': isim[1],
            'İniş': isim[2],
            'Ham Ortalama': round(ham_ortalama, 2),
            'Temiz Ortalama': round(temiz_ortalama, 2),
            'Toplam Veri': toplam_veri,
            'Aykırı Veri': aykiri_veri
        })
        
        # Veritabanına kaydetmek için model objesi oluştur
        yeni_ozet = GunlukOzet(
            hat_kodu=isim[0],
            binis_duragi=isim[1],
            inis_duragi=isim[2],
            temiz_ortalama=round(temiz_ortalama.item(), 2), 
            toplam_veri_sayisi=toplam_veri,
            aykiri_veri_sayisi=aykiri_veri
        )
        db.add(yeni_ozet)

    # Tüm yeni özetleri veritabanına işle
    db.commit()
    db.close()

    # Sonuç Raporunu Ekrana Yazdır
    sonuc_df = pd.DataFrame(temizlenmis_veriler)
    print("\n--- GÜN SONU ANALİZ VE TEMİZLİK RAPORU ---")
    print(sonuc_df.to_string(index=False))
    print("\nVeriler başarıyla 'gunluk_ozetler' tablosuna kaydedildi.")

if __name__ == "__main__":
    gun_sonu_analizi_ve_temizlik()