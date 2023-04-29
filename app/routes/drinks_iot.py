from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os

import boto3
router = APIRouter()

@router.get("/serve/{drink_id}")
async def read_item(drink_id: str):
    
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
            payload="{'drink': '"+drink_id+"'}"
        )
    except Exception as error:
        print(error)
        return JSONResponse(content={"error": "error sending request"}, status_code=500)
        
        
        
    
    
    return JSONResponse(content={"data": response}, status_code=200)

@router.get("/")
async def read_item():
    
    return JSONResponse(content={"data": "working"}, status_code=200)