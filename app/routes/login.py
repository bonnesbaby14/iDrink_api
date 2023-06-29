from fastapi import APIRouter, Depends

from ..database import get_db_session
from ..models import User
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import status
from fastapi import HTTPException
router = APIRouter()



class UserRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(user: UserRequest,session: Session = Depends(get_db_session)):


   
        
    userDB = session.query(User).filter(User.email == user.email).first()
    if not userDB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    if userDB.password!=user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    access_token = "token"
    return {"access_token": access_token, "token_type": "bearer","name":userDB.full_name}        

class NewUserNormalRequest(BaseModel):
    email: str
    password: str
    name:str
    phone:str
    
    
@router.post("/register_normal")
async def register(user:NewUserNormalRequest,session: Session = Depends(get_db_session)):
    pass
   

