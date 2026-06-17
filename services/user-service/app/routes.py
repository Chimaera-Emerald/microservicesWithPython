from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserOut, UserList
from app import service

router = APIRouter(prefix="/v1/users")

@router.post("/", response_model=UserOut, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return service.add_user(db, data)

@router.get("/", response_model=UserList)
def list_users(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    return service.fetch_all_users(db, limit, offset)

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, db: Session = Depends(get_db)):
    try:
        return service.fetch_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
