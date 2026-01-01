from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class ErrorLog(Base):
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    message = Column(Text, nullable=False)
    error_type = Column(String(100), nullable=True, index=True)
    project = Column(String(255), nullable=True, index=True)
    git_branch = Column(String(255), nullable=True)
    git_commit = Column(String(40), nullable=True)
    os = Column(String(50), nullable=True)
    language = Column(String(50), nullable=True, index=True)
    tags = Column(ARRAY(String), nullable=True)
    solution = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    time_to_fix_min = Column(Integer, nullable=True)
    resolved = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="errors")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, index=True, nullable=False)
    github_username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    access_token = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    errors = relationship("ErrorLog", back_populates="user")
