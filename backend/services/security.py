from datetime import datetime, timedelta
from jose import jwt
import bcrypt
from dotenv import load_dotenv
load_dotenv()
import os


SECRET_KEY = os.getenv('SC')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 60


#fonction pour hasher le mot de passe avec bcrypt
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()                 # génère un salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')           # convertir bytes → string pour stockage


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Tronquer et encoder le mot de passe en clair
    password_bytes = plain_password.encode("utf-8")[:72]
    # Comparer avec le hash existant
    return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
