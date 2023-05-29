from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi.encoders import jsonable_encoder
import os
from ..database import session
from ..models import Status
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

        # Generar gráfica de barras con colores personalizados
        colors = ['blue', 'green', 'red', 'yellow']
        ax = df.plot(kind='bar', color=colors)
        ax.set_xlabel('Botellas')
        ax.set_ylabel('mililitros')
        ax.set_title('Niveles de botellas')

        # Agregar leyenda con los valores de cada color
        legend_labels = ['Valor 1', 'Valor 2', 'Valor 3', 'Valor 4']
        ax.legend(legend_labels, loc='upper right')

        # Convertir la gráfica a una imagen en formato Base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()

        return JSONResponse(content={"data": jsonable_encoder(status), "image_base64": "data:image/png;base64," + image_base64}, status_code=200)
    else:
        return JSONResponse(content={"message": "No records found"}, status_code=404)