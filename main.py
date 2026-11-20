from fastapi import FastAPI,Request,Response
from fastapi.templating import Jinja2Templates
from model import Student
from database import engine,Base,SessionLocal,getdb
from sqlalchemy.orm import session

app=FastAPI()
Base.metadata.create_all(bind=engine)

templates=Jinja2Templates(directory="templates")
@app.get("/")
def home(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )
# @app.post("/login")
# def login(request:Request):
#     return templates.TemplateResponse(
#         request=request,
#         name="login.html"
#     )
@app.get("/login")
def login(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )
@app.get("/register")
def login(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="regis.html"
    )