from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime
import os
from ..database import session
from ..models import Order
import boto3
router = APIRouter()

@router.post("/serve")
async def store_order(drink:str, user:str):
    
    try:
        client = boto3.client(
        'iot-data',
        region_name='us-east-1',
        aws_access_key_id='AKIASRAESISWM5GTTZMU',
        aws_secret_access_key='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'
        )
    except Exception as error:
        print(error)
        return JSONResponse(content={"error": "error creating client boto"}, status_code=500)
        
        
    try:
        response = client.publish(
            topic="esp32/sub",
            qos=0,
            payload="{'drink': '"+drink+"'}"
        )
    except Exception as error:
        print(error)
        return JSONResponse(content={"error": "error sending request"}, status_code=500)
        
    order = Order(drink=drink, user=user, created_at=datetime.now())
    session.add(order)
    session.commit()
    session.refresh(order)
        
    
    
    return JSONResponse(content={"data": response}, status_code=200)

@router.get("/")
async def read_item():
    
    return JSONResponse(content={"data": "working"}, status_code=200)