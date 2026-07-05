from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # CORS eklentisi içeri aktarıldı
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI(
    title="Toplu Taşıma Yoğunluk Takibi API",
    description="Kitle kaynaklı veri toplama ve yoğunluk analizi backend servisi",
    version="1.0.0"
)

# CORS Ayarları (Frontend'in API ile konuşmasına izin veriyoruz)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme aşamasında her kaynağa açık.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... (Kodun geri kalanı, modeller ve uç noktalar aynı kalacak) ...


# Pydantic Modeli
class DensityReport(BaseModel):
    user_id: str = Field(..., description="Kullanıcının benzersiz ID bilgisi")
    route_code: str = Field("KADIKOY-PENDIK-MAVI", description="Dolmuş hat kodu")
    density_status: str = Field(..., description="SAKIN, YOGUN veya COK_YOGUN")
    latitude: float = Field(..., description="Kullanıcının anlık enlemi")
    longitude: float = Field(..., description="Kullanıcının anlık boylamı")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Verinin üretilme zamanı")


# Geçici Veri Yapıları (Gerçek projede Redis veya PostgreSQL kullanılacak)
temporary_memory = []
user_last_report_time = {}  # Spam kontrolü için { "user_id": datetime }

# Yoğunluk skorlama haritası
SCORE_MAP = {
    "SAKIN": 1,
    "YOGUN": 2,
    "COK_YOGUN": 3
}


@app.get("/")
def read_root():
    return {"status": "Sistem Aktif", "pilot_hat": "Kadikoy - Pendik (Mavi Minibus)"}


@app.post("/api/v1/density-report", status_code=201)
def receive_density_report(report: DensityReport):
    current_time = datetime.utcnow()
    valid_statuses = ["SAKIN", "YOGUN", "COK_YOGUN"]

    if report.density_status.upper() not in valid_statuses:
        raise HTTPException(status_code=400, detail="Geçersiz yoğunluk durumu.")

    # 1. SPAM FİLTRESİ
    # Kullanıcı son 5 dakika içinde tekrar veri göndermeye çalışırsa engelle
    if report.user_id in user_last_report_time:
        last_time = user_last_report_time[report.user_id]
        if current_time - last_time < timedelta(minutes=5):
            raise HTTPException(status_code=429, detail="Spam Filtresi: Lütfen yeni bir bildirim için bekleyin.")

    # Geçerli bildirimi belleğe ve spam kontrolcüsüne ekle
    user_last_report_time[report.user_id] = current_time
    report_dict = report.model_dump()
    temporary_memory.append(report_dict)

    return {
        "message": "Bildirim başarıyla sisteme işlendi.",
        "processed_at": current_time,
        "recorded_status": report.density_status
    }


# Hat durumunu hesaplayan yeni uç nokta
@app.get("/api/v1/route-status/{route_code}")
def get_route_status(route_code: str):
    current_time = datetime.utcnow()

    # 2. ZAMAN FİLTRESİ (Son 15 dakikanın verilerini al)
    recent_reports = [
        rep for rep in temporary_memory
        if rep["route_code"] == route_code and (current_time - rep["timestamp"]) <= timedelta(minutes=15)
    ]

    if not recent_reports:
        return {"route_code": route_code, "status": "VERI_YOK", "average_score": 0, "report_count": 0}

    # 3. BASİT ORTALAMA HESABI
    total_score = sum(SCORE_MAP[rep["density_status"]] for rep in recent_reports)
    avg_score = total_score / len(recent_reports)

    # Nihai durumu belirle
    if avg_score < 1.5:
        final_status = "SAKIN"
    elif avg_score < 2.5:
        final_status = "YOGUN"
    else:
        final_status = "COK_YOGUN"

    return {
        "route_code": route_code,
        "status": final_status,
        "average_score": round(avg_score, 2),
        "report_count": len(recent_reports)
    }