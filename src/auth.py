from datetime import datetime, timedelta, timezone
from typing import Optional
from  config import settings
from fastapi import HTTPException

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


# Contexte de hachage pour les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modèle Pydantic pour le token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Fonction pour vérifier le mot de passe
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Fonction pour hacher le mot de passe
def get_password_hash(password):
    return pwd_context.hash(password)

# Fonction pour créer un token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc)  + timedelta(minutes=15)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Fonction pour décoder et vérifier le token JWT
def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise JWTError
        token_data = TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=401, detail={"msg":"invalid token or expired token","status":401})

    return token_data