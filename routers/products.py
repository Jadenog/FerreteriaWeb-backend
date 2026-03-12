from fastapi import APIRouter, HTTPException, status
from db.models.products import Product
from db.client import db_client
from db.schemas.products import product_schema, products_schema
from bson import ObjectId
from passlib.context import CryptContext

router = APIRouter(prefix="/products", tags=["products"], responses={404: {"description": "Not found"}})