from fastapi import APIRouter
import boto3
router = APIRouter()

@router.get("/serve/{drink_id}")
async def read_item(drink_id: int, q: str = None):
    
    try:
        client = boto3.client(
        'iot-data',
        region_name='us-east-1',
        aws_access_key_id='AKIASRAESISWBM7NUMZ6',
        aws_secret_access_key='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'
        )
    except:
        return {"messege":"error creating client boto"}
        
    try:
        response = client.publish(
            topic="esp32/sub",
            qos=0,
            payload="{'message': 'Lo saludamos desde la fastapi'}"
        )
    except:
        return {"messege":"error sending request"}
        
        
    
    
    return {"drink_id": drink_id, "q": q}

@router.get("/")
async def read_item():
    print("etre")
    return {"drink_id":"hola"}