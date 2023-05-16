from fastapi import FastAPI

from .routes import drinks_iot
from .routes import login
from .routes import status

# Crea una instancia de FastAPI
app = FastAPI()

# Agrega middlewares, dependencias globales, configuraciones de bases de datos, etc.
# ...

# Importa las rutas desde el archivo routes.py


# Agrega las rutas a la aplicación
app.include_router(drinks_iot.router)
app.include_router(login.router)
app.include_router(status.router)


# print("listo")