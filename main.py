from fastapi import FastAPI
from routers import login, products, users, news, orders
from fastapi.staticfiles import StaticFiles

# python -m uvicorn main:app --reload  --> para ejecutar el servidor de desarrollo, con recarga automática
app = FastAPI()

#routers
app.include_router(users.router)
app.include_router(login.router) 
app.include_router(products.router)
app.include_router(news.router)
app.include_router(orders.router)