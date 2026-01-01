import os
from typing import List, Optional

import httpx
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_user, get_or_create_user, oauth
from database import Base, engine, get_db
from db_utils import create_database_if_not_exists
from models import ErrorLog, User
from schemas import (
    ErrorLogCreate,
    ErrorLogResponse,
    ErrorLogUpdate,
    TokenResponse,
    UserResponse,
)

create_database_if_not_exists()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI PostgreSQL Starter with GitHub OAuth",
    description="A FastAPI application with PostgreSQL and GitHub OAuth authentication",
    version="2.0.0",
)

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "your-secret-key-change-in-production"),
)


@app.get("/")
def read_root() -> dict:
    return {"message": "Welcome to FastAPI with PostgreSQL and GitHub OAuth"}


@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}


@app.get("/auth/login")
async def login(request: Request) -> RedirectResponse:
    redirect_uri = request.url_for("auth_callback")
    return await oauth.github.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)) -> RedirectResponse:
    try:
        token = await oauth.github.authorize_access_token(request)

        access_token = token.get("access_token")
        if not access_token:
            return RedirectResponse(url=f"{FRONTEND_URL}/auth/callback?error=Failed to get access token")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            github_data = response.json()

        github_id = github_data.get("id")
        if not github_id:
            return RedirectResponse(url=f"{FRONTEND_URL}/auth/callback?error=Failed to get GitHub user data")

        user = get_or_create_user(db, github_id, github_data, access_token)

        jwt_token = create_access_token(data={"sub": str(user.id)})

        return RedirectResponse(url=f"{FRONTEND_URL}/auth/callback?token={jwt_token}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/callback?error={str(e)}")


@app.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@app.get("/users/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[User]:
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Error CRUD endpoints
@app.get("/errors/", response_model=List[ErrorLogResponse])
def get_errors(
    skip: int = 0,
    limit: int = 100,
    project: Optional[str] = Query(None, description="Filter by project"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    resolved: Optional[bool] = Query(None, description="Filter by resolved status"),
    language: Optional[str] = Query(None, description="Filter by language"),
    error_type: Optional[str] = Query(None, description="Filter by error type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[ErrorLog]:
    query = db.query(ErrorLog).filter(ErrorLog.user_id == current_user.id)

    if project:
        query = query.filter(ErrorLog.project == project)
    if tag:
        query = query.filter(ErrorLog.tags.contains([tag]))
    if resolved is not None:
        query = query.filter(ErrorLog.resolved == resolved)
    if language:
        query = query.filter(ErrorLog.language == language)
    if error_type:
        query = query.filter(ErrorLog.error_type == error_type)

    return query.order_by(ErrorLog.created_at.desc()).offset(skip).limit(limit).all()


@app.get("/errors/{error_id}", response_model=ErrorLogResponse)
def get_error(
    error_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ErrorLog:
    error = db.query(ErrorLog).filter(
        ErrorLog.id == error_id,
        ErrorLog.user_id == current_user.id,
    ).first()
    if error is None:
        raise HTTPException(status_code=404, detail="Error not found")
    return error


@app.post("/errors/", response_model=ErrorLogResponse, status_code=201)
def create_error(
    error: ErrorLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ErrorLog:
    db_error = ErrorLog(**error.model_dump(), user_id=current_user.id)
    db.add(db_error)
    db.commit()
    db.refresh(db_error)
    return db_error


@app.put("/errors/{error_id}", response_model=ErrorLogResponse)
def update_error(
    error_id: int,
    error: ErrorLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ErrorLog:
    db_error = db.query(ErrorLog).filter(
        ErrorLog.id == error_id,
        ErrorLog.user_id == current_user.id,
    ).first()
    if db_error is None:
        raise HTTPException(status_code=404, detail="Error not found")

    update_data = error.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_error, field, value)

    db.commit()
    db.refresh(db_error)
    return db_error


@app.delete("/errors/{error_id}", status_code=204)
def delete_error(
    error_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    db_error = db.query(ErrorLog).filter(
        ErrorLog.id == error_id,
        ErrorLog.user_id == current_user.id,
    ).first()
    if db_error is None:
        raise HTTPException(status_code=404, detail="Error not found")

    db.delete(db_error)
    db.commit()
    return None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
