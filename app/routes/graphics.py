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
from fastapi.responses import FileResponse
import tempfile
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



@router.get("/export_status")
async def export_status():
    status = session.query(Status).order_by(Status.id.desc()).all()

    # Crear el DataFrame a partir de los resultados de la consulta
    df = pd.DataFrame.from_records([s.__dict__ for s in status])

    # Eliminar la columna '_sa_instance_state' que no es necesaria
    df = df.drop('_sa_instance_state', axis=1)

    # Exportar el DataFrame a un archivo temporal de Excel
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=True) as temp_file:
        excel_filename = temp_file.name
        df.to_excel(excel_filename, index=False)

        # Retornar el archivo de Excel en la respuesta de la API
        temp_file.flush()  # Asegurarse de que el archivo se guarde en el disco
        
        temp_file.seek(0)  # Asegurarse de que el archivo esté en la posición inicial
        return FileResponse(temp_file.name, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename='status_data.xlsx')
    
@router.get("/export_orders")
async def export_orders():
    orders = session.query(Order).all()

    # Crear el DataFrame a partir de los resultados de la consulta
    df = pd.DataFrame.from_records([order.__dict__ for order in orders])

    # Eliminar la columna '_sa_instance_state' que no es necesaria
    df = df.drop('_sa_instance_state', axis=1)

    # Exportar el DataFrame a un archivo temporal de Excel
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=True) as temp_file:
        excel_filename = temp_file.name
        df.to_excel(excel_filename, index=False)

        # Retornar el archivo de Excel en la respuesta de la API
        temp_file.flush()
        temp_file.seek(0)  # Asegurarse de que el archivo esté en la posición inicial
        return FileResponse(temp_file.name, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename='orders_data.xlsx')
    