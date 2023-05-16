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
from pydantic import BaseModel

router = APIRouter()




@router.get("/status")
async def read_item():
    
    status = session.query(Status).order_by(desc(Status.created_at)).first()
   
    return JSONResponse(content={"data": jsonable_encoder(status)}, status_code=200)