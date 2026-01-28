from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from pydantic import field_validator, ConfigDict
from typing import Optional
import re

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str = ""
    full_name: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True
    is_superuser: bool = False
    
    @property
    def is_admin(self) -> bool:
        return self.is_superuser
    
    @property
    def created_days_ago(self) -> int:
        return (datetime.now(timezone.utc) - self.created_at).days
    
    def get_display_name(self) -> str:
        if self.full_name.strip():
            return self.full_name
        return self.email.split('@')[0]
    
    def is_account_older_than(self, days: int) -> bool:
        return self.created_days_ago > days
    
    def deactivate(self):
        self.is_active = False
    
    def activate(self):
        self.is_active = True

class UserBase(SQLModel):
    email: str
    full_name: str = Field(min_length=1, max_length=100)
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Email inválido")
        return v.lower()

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=50)
    
    @field_validator('password')
    @classmethod
    def validate_password_bytes(cls, v: str) -> str:
        password_bytes = v.encode('utf-8')
        if len(password_bytes) > 72:
            raise ValueError("Senha muito longa (limite: ~72 caracteres ASCII ou menos se usar acentos)")
        return v

class UserUpdate(SQLModel):
    email: Optional[str] = None
    full_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    password: Optional[str] = Field(default=None, min_length=8, max_length=50)
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(pattern, v):
                raise ValueError("Email inválido")
            return v.lower()
        return v

class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime