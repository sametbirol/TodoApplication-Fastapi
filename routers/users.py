from .auth import get_current_user, get_password_hash, verify_password,templates
from fastapi import Depends, APIRouter,Form,Request,status
from pydantic import BaseModel
from typing import Optional
import models
from sqlalchemy.orm import Session
from database import SessionLocal,engine
from starlette.responses import RedirectResponse

from fastapi.responses import HTMLResponse

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={401: {"user": "Not authenticated"}}
)
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
# class CreateUser(BaseModel):
#     username: str
#     email: Optional[str]
#     first_name: str
#     last_name: str
#     password: str

@router.get("/", response_class=HTMLResponse)
async def password_change_page(request: Request):
    return templates.TemplateResponse("password.html", {"request": request})

@router.post("/passwordchange",response_class=HTMLResponse)
async def change_password(request:Request,username:str=Form(),password:str=Form(),password2:str=Form(),db:Session=Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    if user_model is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    if verify_password(password,user_model.hashed_password):
        user_model.hashed_password = get_password_hash(password2)
        db.add(user_model)
        db.commit()
        msg = "Password change succsessful"
        return RedirectResponse(url="/auth/logout", status_code=status.HTTP_302_FOUND)
    msg = "password is not correct"
    return templates.TemplateResponse("password.html",{"request":request,"msg":msg})

# router = APIRouter(
#     prefix="/user",
#     tags=["user"],
#     responses={401: {"user": "Not authenticated"}}
# )


# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


# class UserVerification(BaseModel):
#     username: str
#     password: str
#     new_password: str


# @router.get("/readall")
# async def read_all(db: Session = Depends(get_db)):
#     return db.query(models.Users).all()


# @router.get("/hello/{user_id}")
# async def read_user_path(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.Users).filter(models.Users.id == user_id).first()
#     if user is None:
#         raise http_exception(404, "user not found")
#     return {"username": user.username, "id": user.id}


# @router.get("/")
# async def read_user_query(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.Users).filter(models.Users.id == user_id).first()
#     if user is None:
#         raise http_exception(404, "user not found")
#     return {"username": user.username, "id": user.id}


# @router.put("/")
# async def update_user(user_password_form: UserVerification, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception
#     user_model = db.query(models.Users).filter(
#         models.Users.id == user.get("id")).first()
#     if user_model is not None:
#         if user_password_form.username == user_model.username and verify_password(user_password_form.password, user_model.hashed_password):
#             user_model.hashed_password = get_password_hash(
#                 user_password_form.new_password)
#             db.add(user_model)
#             db.commit()
#         return succesful_response(200)
#     raise http_exception(404, "user not found")


# @router.delete("/{user_id}")
# async def delete_user(user_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception
#     user_model = db.query(models.Users).filter(models.Users.id == user_id).filter(
#         models.Users.id == user.get("id")).first()
#     if user_model is None:
#         raise http_exception(404, "user not found")
#     db.delete(user_model)
#     db.commit()
#     return succesful_response(200)
