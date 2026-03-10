from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})

#funciones
def search_user(fiel: str, key):
    try:
        user = db_client.users.find_one({fiel: key})
        return User(**user_schema(user))
    except:
        return { "Error": "no ha sido posible encontrar el usuario" }
    
#endpoints    
#agregar un nuevo usuario
@router.post("/",response_model=User, status_code=201)# manejo de codigos/errores http, en este caso 201 es creado
async def user(user: User):
        if type(search_user("email", user.email)) == User:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")# si el usuario ya existe, devolvemos un error 204, que significa que no se ha podido crear el recurso porque ya existe
        user_dict = dict(user)
        del user_dict["id"] # eliminamos el id del diccionario, porque lo vamos a generar automáticamente con MongoDB, que genera un id único para cada documento
        id = db_client.users.insert_one(user_dict).inserted_id #insertamos el usuario en la base de datos, utilizando el cliente de la base de datos y la colección de usuarios
        new_user = user_schema(db_client.users.find_one({"_id": id})) #buscamos el usuario recién insertado en la base de datos, utilizando el id generado por MongoDB
        return User(**new_user) 

#obtener usuarios
@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())