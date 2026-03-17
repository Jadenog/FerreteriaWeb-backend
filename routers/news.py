from fastapi import APIRouter, HTTPException, status
from db.models.news import New
from db.client import db_client
from db.schemas.new import news_schema, new_schema
from bson import ObjectId


router = APIRouter(prefix="/news", tags=["news"], responses={404: {"description": "Not found"}})

#lista de noticias
@router.get("/", response_model=list[New], status_code=status.HTTP_200_OK)
async def news():
    return news_schema(db_client.news.find())

#obtener un new por id
@router.get("/{id}", response_model=news, status_code=status.HTTP_200_OK)
async def new(id: str):
    return news_schema(db_client.news.find_one({"_id": ObjectId(id)}))

#agregar un nuevo new
@router.post("/", response_model=New, status_code=status.HTTP_201_CREATED)
async def create_new(new: New):
    new_dict = new.dict()
    result = db_client.news.insert_one(new_dict)
    return new_schema(db_client.news.find_one({"_id": result.inserted_id}))

#actualizar un producto por id
@router.put("/{id}", response_model=New, status_code=status.HTTP_202_ACCEPTED)
async def update_new(id: str, new: New):
    new_dict = new.dict()
    db_client.news.update_one({"_id": ObjectId(id)}, {"$set": new_dict})
    return new_schema(db_client.news.find_one({"_id": ObjectId(id)}))

#eliminar un producto por id
@router.delete("/{id}")
async def delete_new(id: str, status_code=status.HTTP_204_NO_CONTENT):
        
        found = db_client.news.find_one_and_delete({"_id": ObjectId(id)})

        if not found:
            return {"error": "Producto no encontrado"}