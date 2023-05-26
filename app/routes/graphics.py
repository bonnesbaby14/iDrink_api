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

router = APIRouter()




@router.get("/graphics_status")
async def read_item():
    status = session.query(Status).all()
    df = pd.DataFrame(status.fetchall(), columns=status.keys())
   
    return JSONResponse(content={"data": jsonable_encoder(status)}, status_code=200)