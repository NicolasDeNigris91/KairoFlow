from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.user import User, UserCreate, UserRead
from app.services.auth import get_password_hash, verify_password, create_access_token
from app.core.database import get_session
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register_user(user_data: UserCreate, db: Session = Depends(get_session)):
    statement = select(User).where(User.email == user_data.email)
    existing_user = db.exec(statement).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    hashed_password = get_password_hash(user_data.password)
    
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login")
def login_user(
    email: str,
    password: str,
    db: Session = Depends(get_session)
):
    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    access_token_expires = timedelta(days=30)
    access_token = create_access_token(
        user=user,
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": access_token_expires.total_seconds(),
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    }