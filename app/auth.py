import hashlib,hmac,secrets,os
from datetime import datetime,timedelta,timezone
from jose import jwt
from fastapi import Request,HTTPException,status
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY","development-secret-change-me")
ALGORITHM="HS256"
EXPIRE=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","60"))

def hash_password(password):
    salt=secrets.token_bytes(16)
    digest=hashlib.pbkdf2_hmac("sha256",password.encode(),salt,120000)
    return f"pbkdf2_sha256$120000${salt.hex()}${digest.hex()}"

def verify_password(password,stored):
    try:
        alg,rounds,salt,digest=stored.split("$")
        d=hashlib.pbkdf2_hmac("sha256",password.encode(),bytes.fromhex(salt),int(rounds))
        return alg=="pbkdf2_sha256" and hmac.compare_digest(d.hex(),digest)
    except Exception: return False

def token(username):
    exp=datetime.now(timezone.utc)+timedelta(minutes=EXPIRE)
    return jwt.encode({"sub":username,"exp":exp},SECRET_KEY,algorithm=ALGORITHM)

def username_from_request(request:Request):
    t=request.cookies.get("access_token")
    if not t: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please sign in.")
    try:
        p=jwt.decode(t,SECRET_KEY,algorithms=[ALGORITHM])
        if not p.get("sub"): raise ValueError()
        return p["sub"]
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Session expired.")
