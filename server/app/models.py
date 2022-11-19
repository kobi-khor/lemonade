
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from email_validator import validate_email
from pydantic import BaseModel, Field, EmailStr, validator
from pydantic.types import constr


# Post Schema
class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(default=None)
    content: str = Field(default=None)

    class Config:
        schema_extra = {
            "post_demo": {
                "title": "some title about animals",
                "content": "some content about animals"
            }
        }


# User Schema
class UserSchema(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    organization_name: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: constr(min_length=8)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    class Config:
        schema_extra = {
            "demo_user": {
                "id": "47aeabdd-cf86-4514-98c9-1c5bad9432be",
                "first_name": "Luci",
                "last_name": "Ruiz",
                "organization_name": "Apple",
                "email": "Ruizlui@gmail.com",
                "created_at": None,
                "updated_at": None,
                "password": "1234567",
                "verified": False,

            }
        }

    @validator('email')
    def email_validation(cls, email):
        email_object = validate_email(email)
        return email_object.email


class CreateUserSchema(UserSchema):
    passwordConfirm: str
    verified: bool = False


# User Login Schema
class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class Config:
        schema_extra = {
            "demo_user": {
                "email": "Ruizlui@gmail.com",
                "password": "12345678",
            }
        }
