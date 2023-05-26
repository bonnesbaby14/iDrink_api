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
        
    
    
    return JSONResponse(content={"data": response}, status_code=200)

@router.get("/")
async def read_item():
    orders = session.query(Order).all()
   
    return JSONResponse(content={"data": jsonable_encoder(orders)}, status_code=200)