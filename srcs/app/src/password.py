from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import os

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

with open(os.getenv('KEY_FILE'), 'r') as f:
    KEY = f.read().strip()
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

def hash_password(password):
    return bcrypt.hash(password)

def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)

def create_access_token(user_id):
    expires = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    data = {"sub": user_id, "exp": expires}
    return jwt.encode(data, KEY, algorithm=ALGORITHM)

def verify_token(token):
    payload = jwt.decode(token, KEY, algorithms=[ALGORITHM])
    return payload["sub"]