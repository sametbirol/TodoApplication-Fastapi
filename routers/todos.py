from routers.auth import get_current_user

from typing import Optional
from fastapi import Depends, Form, HTTPException, APIRouter, Request
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.responses import RedirectResponse


router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}}
)
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todos = db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()

    return templates.TemplateResponse("home.html", {"request": request, "todos": todos,"user":user})


@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("add-todo.html", {"request": request,"user":user})


@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(), description: str = Form(), priority: int = Form(), db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo_model = models.Todos()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.complete = False
    todo_model.owner_id = user.get("id")
    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(todo_id: int, request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(
        models.Todos.owner_id == user.get("id")
        ).first()
    if todo is None:
        raise HTTPException(status_code=404,detail="todo not found")
    return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo,"user":user})


@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_commit(request: Request, todo_id: int, title: str = Form(...),
                           description: str = Form(...), priority: int = Form(...),
                           db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo_model = db.query(models.Todos).filter(
        models.Todos.id == todo_id).filter(
        models.Todos.owner_id == user.get("id")
        ).first()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/delete/{todo_id}", response_class=HTMLResponse)
async def delete_todo(todo_id: int, request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo = db.query(models.Todos).filter(models.Todos.id ==
                                         todo_id).filter(
        models.Todos.owner_id == user.get("id")
        ).first()
    if todo is None:
        return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
    db.delete(todo)
    db.commit()
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/complete/{todo_id}", response_class=HTMLResponse)
async def complete_todo(todo_id: int, request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
  
    
    todo = db.query(models.Todos).filter(models.Todos.id ==
                                         todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo is None:
        return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
    todo.complete = not todo.complete
    db.add(todo)
    db.commit()
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)