from fastapi import APIRouter, HTTPException, status, Depends
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter(prefix="/login", tags=["login"], responses={404: {"description": "Not found"}})


# ==============================
# Configuración
# ==============================

SECRET_KEY = "d7e87e274bfdc384a39836096de9ca641999bda2d686ac3196b54c3032207896" # generado en cmd con el comando openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 3  # minutos


oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==============================
# Funciones auxiliares
# ==============================

def search_user(name: str):
    user = db_client.users.find_one({"name": name})
    if user:
        return User(**user_schema(user))
    return None


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")

        if name is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = search_user(name)

    if user is None:
        raise credentials_exception


    return user


# ==============================
# Login
# ==============================

@router.post("/")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    user = search_user(form.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario incorrecto"
        )

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña incorrecta"
        )

    access_token = create_access_token({"sub": user.name})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ==============================
# Ruta protegida
# ==============================

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user