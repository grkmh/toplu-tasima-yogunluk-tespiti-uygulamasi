from datetime import datetime, timedelta, timezone
import os

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Kullanici


SECRET_KEY = os.getenv("SECRET_KEY", "gelistirmede-degistirilecek-rotaradar-anahtari")
ALGORITHM = "HS256"
TOKEN_SURESI_SAAT = 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer = HTTPBearer(auto_error=False)


def parola_hashle(parola: str) -> str:
    return pwd_context.hash(parola)


def parola_dogrula(parola: str, parola_hash: str) -> bool:
    return pwd_context.verify(parola, parola_hash)


def token_olustur(kullanici_id: int) -> str:
    son_kullanma = datetime.now(timezone.utc) + timedelta(hours=TOKEN_SURESI_SAAT)
    return jwt.encode(
        {"sub": str(kullanici_id), "exp": son_kullanma},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def aktif_kullanici(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> Kullanici:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Giriş yapmanız gerekiyor.")

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        kullanici_id = int(payload["sub"])
    except (InvalidTokenError, KeyError, TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Oturum geçersiz veya süresi dolmuş.")

    kullanici = db.query(Kullanici).filter(Kullanici.id == kullanici_id).first()
    if kullanici is None:
        raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı.")
    return kullanici
