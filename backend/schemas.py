from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ErrorLogBase(BaseModel):
    message: str
    error_type: Optional[str] = None
    project: Optional[str] = None
    git_branch: Optional[str] = None
    git_commit: Optional[str] = None
    os: Optional[str] = None
    language: Optional[str] = None
    tags: Optional[list[str]] = None
    solution: Optional[str] = None
    notes: Optional[str] = None
    time_to_fix_min: Optional[int] = None
    resolved: bool = False


class ErrorLogCreate(ErrorLogBase):
    pass


class ErrorLogUpdate(BaseModel):
    message: Optional[str] = None
    error_type: Optional[str] = None
    project: Optional[str] = None
    git_branch: Optional[str] = None
    git_commit: Optional[str] = None
    os: Optional[str] = None
    language: Optional[str] = None
    tags: Optional[list[str]] = None
    solution: Optional[str] = None
    notes: Optional[str] = None
    time_to_fix_min: Optional[int] = None
    resolved: Optional[bool] = None


class ErrorLogResponse(ErrorLogBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    github_id: int
    github_username: str
    email: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
