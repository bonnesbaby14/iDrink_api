from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi.encoders import jsonable_encoder
import os
from ..database import session
from ..models import Status
from ..models import Order
from typing import Dict
import boto3
from sqlalchemy import desc
import pandas as pd
from pydantic import BaseModel
import io
import base64
import matplotlib.pyplot as plt

router = APIRouter()




@router.get("/graphics_status")
async def read_item():
    status = session.query(Status).order_by(Status.id.desc()).first()

    if status:
        values = [float(status.bottle1), float(status.bottle2), float(status.bottle3), float(status.bottle4)]
        labels = ['Bottle 1', 'Bottle 2', 'Bottle 3', 'Bottle 4']

        df = pd.DataFrame({'Botellas': values}, index=labels)

        # Generar gráfica de barras
        ax = df.plot(kind='bar')
        ax.set_xlabel('Botellas')
        ax.set_ylabel('mililitros')
        ax.set_title('Niveles de botellas')

        # Asignar colores personalizados a las barras
        colors = ['blue', 'green', 'red', 'yellow']
        for i, bar in enumerate(ax.patches):
            bar.set_color(colors[i % len(colors)])

        # Agregar leyenda con los valores de cada color
        legend_labels = ['Tequila', 'Vodka', 'Jugo', 'Granadina']
        ax.legend(legend_labels, loc='upper right')

        # Convertir la gráfica a una imagen en formato Base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()

        return JSONResponse(content={"data": jsonable_encoder(status), "image_base64": "data:image/png;base64," + image_base64}, status_code=200)
    else:
        return JSONResponse(content={"message": "No records found"}, status_code=404)
    
    
@router.get("/graphics_orders_users")
async def read_item():
    orders = session.query(Order).all()

    if orders:
        # Crear un diccionario para almacenar la cantidad de bebidas por usuario
        data = {}

        # Contar la cantidad de bebidas por usuario
        for order in orders:
            user = order.user
            drink = order.drink

            if user in data:
                if drink in data[user]:
                    data[user][drink] += 1
                else:
                    data[user][drink] = 1
            else:
                data[user] = {drink: 1}

        # Convertir el diccionario a un DataFrame
        df = pd.DataFrame(data).fillna(0)

        # Generar gráfica de barras apiladas
        ax = df.plot(kind='bar', stacked=True)
        ax.set_xlabel('Usuario')
        ax.set_ylabel('Cantidad de Bebidas')
        ax.set_title('Cantidad de Bebidas por Usuario')

        # Convertir la gráfica a una imagen en formato Base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()

        return JSONResponse(content={"data": jsonable_encoder(data), "image_base64": "data:image/png;base64," + image_base64}, status_code=200)
    else:
        return JSONResponse(content={"message": "No records found"}, status_code=404)
    
@router.get("/graphics_orders")
async def read_item():
    orders = session.query(Order).all()

    if orders:
        # Crear un diccionario para almacenar la cantidad de bebidas
        data = {}

        # Contar la cantidad de bebidas
        for order in orders:
            drink = order.drink

            if drink in data:
                data[drink] += 1
            else:
                data[drink] = 1

        # Convertir el diccionario a un DataFrame
        df = pd.DataFrame(data, index=[0])

        # Generar gráfica de barras
        ax = df.plot(kind='bar')
        ax.set_xlabel('Bebida')
        ax.set_ylabel('Cantidad')
        ax.set_title('Cantidad de Bebidas')

        # Convertir la gráfica a una imagen en formato Base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()

        return JSONResponse(content={"data": jsonable_encoder(data), "image_base64": "data:image/png;base64," + image_base64}, status_code=200)
    else:
        return JSONResponse(content={"message": "No records found"}, status_code=404)
