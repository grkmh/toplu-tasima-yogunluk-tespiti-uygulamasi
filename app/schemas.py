from pydantic import BaseModel, ConfigDict, Field


class KullaniciKayit(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    kullanici_adi: str = Field(
        ..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_.-]+$"
    )
    parola: str = Field(..., min_length=6, max_length=72)


class KullaniciGiris(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    kullanici_adi: str = Field(..., min_length=3, max_length=50)
    parola: str = Field(..., min_length=6, max_length=72)


class YolculukBaslangic(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    hat_kodu: str = Field(..., min_length=1, max_length=20)
    durak_adi: str = Field(..., min_length=2, max_length=100)
    yogunluk_skoru: int = Field(..., ge=1, le=9)


class YolculukBitis(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    durak_adi: str = Field(..., min_length=2, max_length=100)
    yogunluk_skoru: int = Field(..., ge=1, le=9)
