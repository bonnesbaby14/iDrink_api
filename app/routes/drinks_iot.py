from fastapi import APIRouter

router = APIRouter()

@router.get("/serve/{drink_id}")
async def read_item(drink_id: int, q: str = None):
    print("etre")
    return {"drink_id": drink_id, "q": q}

@router.get("/")
async def read_item():
    print("etre")
    return {"drink_id":"hola"}