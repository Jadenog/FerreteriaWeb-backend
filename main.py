from fastapi import FastAPI
from routers import login, users
from fastapi.staticfiles import StaticFiles

# python -m uvicorn main:app --reload  --> para ejecutar el servidor de desarrollo, con recarga automática
app = FastAPI()

#routers
app.include_router(users.router)
app.include_router(login.router) 