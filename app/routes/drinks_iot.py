from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi.encoders import jsonable_encoder
import os
from ..database import session
from ..models import Order
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
        aws_access_key_id='AKIASRAESISWBWECP2OV',
        aws_secret_access_key='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'
        )
    except Exception as error:
        print(error)
        return JSONResponse(content={"error": "error creating client boto"}, status_code=500)
        
        
    try:
        response = client.publish(
            topic="esp32/sub",
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
        
    
    
    return JSONResponse(content={"data": response}, status_code=200)

@router.get("/")
async def read_item():
    orders = session.query(Order).all()
   
    return JSONResponse(content={"data": jsonable_encoder(orders)}, status_code=200)