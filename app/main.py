from fastapi import FastAPI

from .routes import drinks_iot
from .routes import login
from .routes import status
from .routes import graphics

# Crea una instancia de FastAPI
app = FastAPI()

# Agrega middlewares, dependencias globales, configuraciones de bases de datos, etc.
# ...

# Importa las rutas desde el archivo routes.py


# sudo docker  run   -v  .:/app -v ./data:/var/lib/mysql   -p 8000:8000 -p 80:80 -p 8080:8080 -p 3306:3306  idrink_docker

# Agrega las rutas a la aplicación
app.include_router(drinks_iot.router)
app.include_router(login.router)
app.include_router(status.router)
app.include_router(graphics.router)


# print("listo")