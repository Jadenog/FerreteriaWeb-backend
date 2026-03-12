from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})

# Configuración de encriptación de contraseñas
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==============================
# Funciones
# ==============================

def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        if user:
            return User(**user_schema(user))
        return None
    except:
        return None


# ==============================
# Endpoints
# ==============================

# Agregar un nuevo usuario
@router.post("/", response_model=User, status_code=201)
async def create_user(user: User):

    if search_user("email", user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya existe"
        )

    user_dict = dict(user)
    del user_dict["id"]

    # Encriptar contraseña antes de guardar
    user_dict["password"] = crypt.hash(user_dict["password"])

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)


# Obtener todos los usuarios
@router.get("/", response_model=list[User])
async def get_users():
    return users_schema(db_client.users.find())


# Actualizar un usuario
@router.put("/", response_model=User)
async def update_user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    # Si se actualiza contraseña, volver a encriptarla
    if "password" in user_dict:
        user_dict["password"] = crypt.hash(user_dict["password"])

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)},
            user_dict
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No ha sido posible actualizar el usuario"
        )

    return search_user("_id", ObjectId(user.id))


# Eliminar un usuario
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):

    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se ha podido eliminar el usuario"
        )