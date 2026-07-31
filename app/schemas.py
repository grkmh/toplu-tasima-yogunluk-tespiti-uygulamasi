from pydantic import BaseModel, Field
class YolculukBaslangic(BaseModel):
    kullanici_id: str = Field(..., example= "Ahmet")
    hat_kodu: str = Field(..., example= "133GP")
    durak_adi: str = Field(..., example= "Kadıköy")
    yogunluk_skoru: int = Field(..., ge=1, le=9, example= 4)

class YolculukBitis(BaseModel):
    kullanici_id: str = Field(..., example= "Ahmet")
    durak_adi: str = Field(..., example= "Pendik")
    yogunluk_skoru: int = Field(..., ge=1, le=9, example= 8)