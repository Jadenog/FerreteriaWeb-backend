from fastapi import APIRouter, status
from db.models.products import Product
from db.client import db_client
from db.schemas.products import product_schema, products_schema
from bson import ObjectId


router = APIRouter(prefix="/products", tags=["products"], responses={404: {"description": "Not found"}})

#lista de productos
@router.get("/", response_model=list[Product], status_code=status.HTTP_200_OK)
async def products():
    return products_schema(db_client.products.find())

#obtener un producto por id
@router.get("/{id}", response_model=Product, status_code=status.HTTP_200_OK)
async def product(id: str):
    return product_schema(db_client.products.find_one({"_id": ObjectId(id)}))

#agregar un nuevo producto
@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):
    product_dict = product.dict()
    product_dict["price"] = float(product_dict["price"])
    result = db_client.products.insert_one(product_dict)
    return product_schema(db_client.products.find_one({"_id": result.inserted_id}))

#actualizar un producto por id
@router.put("/{id}", response_model=Product, status_code=status.HTTP_202_ACCEPTED)
async def update_product(id: str, product: Product):
    product_dict = product.dict()
    product_dict["price"] = float(product_dict["price"])
    db_client.products.update_one({"_id": ObjectId(id)}, {"$set": product_dict})
    return product_schema(db_client.products.find_one({"_id": ObjectId(id)}))

#eliminar un producto por id
@router.delete("/{id}")
async def product(id: str, status_code=status.HTTP_204_NO_CONTENT):
        
        found = db_client.products.find_one_and_delete({"_id": ObjectId(id)})

        if not found:
            return {"error": "Producto no encontrado"}