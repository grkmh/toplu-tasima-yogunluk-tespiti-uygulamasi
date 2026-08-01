from pydantic import BaseModel, Field


class YolculukBaslangic(BaseModel):
    # Kullanıcı ID: En az 3, en fazla 50 karakter. Sadece harf, rakam ve alt çizgi.
    kullanici_id: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$",
        example="Ahmet_123"
    )

    # Hat Kodu: Boş bırakılamaz (min_length=1), maks 10 karakter. Boşlukla başlayıp bitemez.
    hat_kodu: str = Field(
        ...,
        min_length=1,
        max_length=10,
        pattern=r"^\S(.*\S)?$",
        example="133GP"
    )

    # Durak Adı: En az 2, en fazla 100 karakter. Sadece boşluklardan oluşamaz.
    durak_adi: str = Field(
        ...,
        min_length=2,
        max_length=100,
        pattern=r"^\S(.*\S)?$",
        example="Kadıköy"
    )

    # Yoğunluk Skoru: Görkem'in eklediği gibi 1-9 arasında kalmalı.
    yogunluk_skoru: int = Field(..., ge=1, le=9, example=4)


class YolculukBitis(BaseModel):
    kullanici_id: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$",
        example="Ahmet_123"
    )

    durak_adi: str = Field(
        ...,
        min_length=2,
        max_length=100,
        pattern=r"^\S(.*\S)?$",
        example="Pendik"
    )

    yogunluk_skoru: int = Field(..., ge=1, le=9, example=8)