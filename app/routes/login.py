from fastapi import APIRouter

from ..database import session
from ..models import User
from pydantic import BaseModel
from fastapi import status
from fastapi import HTTPException
router = APIRouter()



class UserRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(user: UserRequest):


   
        
    userDB = session.query(User).filter(User.email == user.email).first()
    if not userDB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    if userDB.password!=user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    access_token = "token"
    return {"access_token": access_token, "token_type": "bearer","name":userDB.full_name}        
    
    
   

