from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.auth import RegisterInput,LoginInput,AuthResponse
from services.security import hash_password,verify_password
router=APIRouter(prefix="/api/auth",tags=["Authentication"])
@router.post("/register",response_model=AuthResponse)
def register(d:RegisterInput,db:Session=Depends(get_db)):
 email=d.email.strip().lower()
 if db.query(User).filter(User.email==email).first(): raise HTTPException(409,"An account with this email already exists.")
 u=User(name=d.name.strip(),email=email,password_hash=hash_password(d.password)); db.add(u); db.commit(); db.refresh(u); return {"user_id":u.id,"name":u.name,"email":u.email}
@router.post("/login",response_model=AuthResponse)
def login(d:LoginInput,db:Session=Depends(get_db)):
 u=db.query(User).filter(User.email==d.email.strip().lower()).first()
 if not u or not verify_password(d.password,u.password_hash): raise HTTPException(401,"Invalid email or password.")
 return {"user_id":u.id,"name":u.name,"email":u.email}
