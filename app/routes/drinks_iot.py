from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi.encoders import jsonable_encoder
import os
from ..database import session
from ..models import Order
from ..models import Status
from typing import Dict
import boto3
from pydantic import BaseModel

router = APIRouter()






class OrderRequest(BaseModel):
    drink: str
    user: str

@router.post("/serve")
async def store_order(order: OrderRequest):




    try:
        client = boto3.client(
        'iot-data',
        region_name='us-east-1',
        aws_access_key_id='AKIASRAESISWID4WF6UP',
        aws_secret_access_key='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'
        )
    except Exception as error:
        print(error)
        return JSONResponse(content={"error": "error creating client boto"}, status_code=500)
        
        
    try:
        response = client.publish(
            topic="IDRINK/sub",
            qos=0,
            payload="{'drink': '"+str(order.drink)+"'}"
        )
    except Exception as error:
        print(error)
        return JSONResponse(content={"error": "error sending request"}, status_code=500)
        
    neworder = Order(drink=order.drink, user=order.user, created_at=datetime.now())
    session.add(neworder)
    session.commit()
    session.refresh(neworder)
    session.close()
    
    
    return JSONResponse(content={"data": response}, status_code=200)

@router.get("/")
async def read_item():
    orders = session.query(Order).all()
    status = session.query(Status).all()
    session.close()
   
    return JSONResponse(content={"data_orders": jsonable_encoder(orders),"data_status":jsonable_encoder(status)}, status_code=200)



class StatusRequest(BaseModel):
    bottle1: str
    bottle2: str
    bottle3: str
    bottle4: str
    
@router.post("/send_leves")
async def receive_data(status: StatusRequest):
    # Realiza las acciones que desees con los valores recibidos
    # Por ejemplo, puedes almacenarlos en la base de datos

    # En este ejemplo, simplemente los devolveremos como respuesta
    
    newstatus = Status(bottle1=status.bottle1, bottle2=status.bottle2, bottle3=status.bottle3,bottle4=status.bottle4,created_at=datetime.now())
    session.add(newstatus)
    session.commit()
    session.refresh(newstatus)
    session.close()
    
    return JSONResponse(content={"status": "ready"}, status_code=200)