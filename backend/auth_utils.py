import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

# 🔑 Clé secrète pour signer les jetons (à personnaliser en production)
SECRET_KEY = "super_cle_secrete_recruitment_match_ol"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # Validité de 24 heures

# --- 1. GESTION DES MOTS DE PASSE ---

def hash_password(password: str) -> str:
    """Transforme un mot de passe en texte clair en un hash sécurisé."""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si le mot de passe entré correspond au hash enregistré."""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# --- 2. GESTION DES JETONS JWT ---

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Génère un jeton JWT contenant les données de l'utilisateur et sa date d'expiration."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """Décode et vérifie la validité d'un jeton JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Le jeton a expiré
    except jwt.InvalidTokenError:
        return None  # Le jeton est invalide

