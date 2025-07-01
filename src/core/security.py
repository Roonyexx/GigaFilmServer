from jose import jwt

SECRET_KEY = "oleg"
ALGORITHM = "HS256"

def createAccessToken(data: dict):
    to_encode = data.copy()
    #todo ограничение токена во времени
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decodeToken(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])