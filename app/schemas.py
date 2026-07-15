from pydantic import BaseModel, Field
class YolculukBaslangic(BaseModel):
    kullanici_id: str = Field(..., example= "İnci")
    hat_kodu: str = Field(..., example= "522ST")
    durak_adi: str = Field(..., example= "Samandıra Kız İmamhatip Lisesi")
    yogunluk_skoru: int = Field(..., ge=1, le=9, example= 4)

class YolculukBitis(BaseModel):
    kullanici_id: str = Field(..., example= "İnci")
    durak_adi: str = Field(..., example= "Kavacık Köprüsü")
    yogunluk_skoru: int = Field(..., ge=1, le=9, example= 8)