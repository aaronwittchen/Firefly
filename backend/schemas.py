from datetime import datetime

from pydantic import BaseModel


class ErrorLogBase(BaseModel):
    message: str
    error_type: str | None = None
    project: str | None = None
    git_branch: str | None = None
    git_commit: str | None = None
    os: str | None = None
    language: str | None = None
    tags: list[str] | None = None
    solution: str | None = None
    notes: str | None = None
    time_to_fix_min: int | None = None
    resolved: bool = False


class ErrorLogCreate(ErrorLogBase):
    pass


class ErrorLogUpdate(BaseModel):
    message: str | None = None
    error_type: str | None = None
    project: str | None = None
    git_branch: str | None = None
    git_commit: str | None = None
    os: str | None = None
    language: str | None = None
    tags: list[str] | None = None
    solution: str | None = None
    notes: str | None = None
    time_to_fix_min: int | None = None
    resolved: bool | None = None


class ErrorLogResponse(ErrorLogBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    github_id: int
    github_username: str
    email: str | None = None
    name: str | None = None
    avatar_url: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
