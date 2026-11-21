from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

from database import get_db, Base, engine
from model import User
from security import hash_password, verify_password


app = FastAPI()

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


# Session Middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="fsd_batch_64_python",
    max_age=300,
    same_site="lax",
    https_only=False
)


# Home Page
@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )


# Register Page
@app.get("/register")
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"error": None}
    )


# Register User
@app.post("/register")
def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "Email already registered"}
        )

    # Hash password
    hashed_password = hash_password(password)

    # Create user
    new_user = User(
        email=email,
        password_hash=hashed_password
    )

    # Save user in database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(
        "/login",
        status_code=303
    )


# Login Page
@app.get("/login")
def login_page(request: Request):

    # Already logged in
    if request.session.get("user_id"):
        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": None}
    )


# Login User
@app.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    # Find user
    user = db.query(User).filter(
        User.email == email
    ).first()

    # Check user exists
    if user is None:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Invalid email or password"}
        )

    # Verify password
    if not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Invalid email or password"}
        )

    # Create session
    request.session["user_id"] = user.id
    request.session["email"] = user.email
    request.session["visit_count"] = 0

    return RedirectResponse(
        "/dashboard",
        status_code=303
    )


# Dashboard
@app.get("/dashboard")
def dashboard(request: Request):

    # Check login
    if "user_id" not in request.session:
        return RedirectResponse(
            "/login",
            status_code=303
        )

    # Get session data
    email = request.session["email"]
    user_id = request.session["user_id"]

    # Increase visit count
    request.session["visit_count"] += 1

    visits = request.session["visit_count"]

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "email": email,
            "user_id": user_id,
            "visits": visits
        }
    )


# Logout
@app.get("/logout")
def logout(request: Request):

    # Clear session
    request.session.clear()

    return RedirectResponse(
        "/",
        status_code=303
    )
