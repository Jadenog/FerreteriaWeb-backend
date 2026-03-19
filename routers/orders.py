from fastapi import APIRouter, status
from db.models.orders import Order
from db.client import db_client
from db.schemas.orders import order_schema, orders_schema
from bson import ObjectId


router = APIRouter(prefix="/orders", tags=["orders"], responses={404: {"description": "Not found"}})

#lista de ordenes
@router.get("/", response_model=list[Order], status_code=status.HTTP_200_OK)
async def orders():
    return orders_schema(db_client.orders.find())

#obtener una orden por id
@router.get("/{id}", response_model=Order, status_code=status.HTTP_200_OK)
async def order(id: str):
    return order_schema(db_client.orders.find_one({"_id": ObjectId(id)}))

#agregar un nueva orden
@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order: Order):
    order_dict = order.dict()
    result = db_client.orders.insert_one(order_dict)
    return order_schema(db_client.orders.find_one({"_id": result.inserted_id}))

#actualizar una orden por id
@router.put("/{id}", response_model=Order, status_code=status.HTTP_202_ACCEPTED)
async def update_order(id: str, order: Order):
    order_dict = order.dict()
    order_dict["total"] = float(order_dict["total"])
    db_client.orders.update_one({"_id": ObjectId(id)}, {"$set": order_dict})
    return order_schema(db_client.orders.find_one({"_id": ObjectId(id)}))

#eliminar una orden por id
@router.delete("/{id}")
async def order(id: str, status_code=status.HTTP_204_NO_CONTENT):
        
        found = db_client.orders.find_one_and_delete({"_id": ObjectId(id)})

        if not found:
            return {"error": "Orden no encontrada"}