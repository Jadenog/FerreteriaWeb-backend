from fastapi import FastAPI
from routers import users
from fastapi.staticfiles import StaticFiles


app = FastAPI()

#routers
app.include_router(users.router)