from datetime import datetime, timedelta
from uuid import UUID

from fastapi import FastAPI, HTTPException, Body, Depends

from app.auth.auth_baerer import JWTBearer
from app.auth.jwt_handler import sign_jwt
from app.models import PostSchema, UserSchema, UserLoginSchema, CreateUserSchema
from app.utils import hash_password, verify_password

posts = [
    {
        "id": 1,
        "title": "penguin",
        "text": "penguin are cute and bla bla bla...."
    },
    {
        "id": 2,
        "title": "dog",
        "text": "dog are stink and cute and bla bla bla...."
    },
    {
        "id": 3,
        "title": "mouse",
        "text": "mouses are cute but  i hate them and wish they all die!"
    }
]

users = [
    {
        "id": UUID("47aeabdd-cf86-4514-98c9-1c5bad9432be"),
        "first_name": "Luci",
        "last_name": "Ruiz",
        "organization_name": "Apple",
        "email": "Ruizlui@gmail.com",
        "created_at": "2022-11-18 19:29:36.646296",
        "updated_at": "2022-11-18 19:29:36.646296",
        "password": "12345678",
        "verified": False
    },
    {
        "id": UUID("444eabdd-cf86-4514-98c9-1c5bad9432be"),
        "first_name": "Ann",
        "last_name": "Bino",
        "organization_name": "Peace.",
        "email": "Annny@gmail.com",
        "created_at": "2022-11-18 19:29:36.646296",
        "updated_at": "2022-11-18 19:29:36.646296",
        "password": "12345888",
        "verified": False
    },
]

app = FastAPI()


@app.get("/", tags=["test"])
def greet():
    return {"Hello": "World"}


@app.get("/posts", tags=["post"])
def get_posts():
    return {"data": posts}


@app.get("/posts/{post_id}", tags=["post"])
def get_post(post_id: int):
    if post_id > len(posts):
        return {
            "error": "Post with this ID does not exist"
        }
    for post in posts:
        if post["id"] == post_id:
            return {
                "data": post
            }
    raise HTTPException(
        status_code=404,
        detail=f"post with id: {post_id} does not exists"
    )


@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["post"])
def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "info": "Post Added"
    }


@app.get("/user", tags=["users"])
def get_users():
    print(type(users))
    return {
        "data": users
    }


@app.get("/user/{user_id}", tags=["users"])
def get_single_user(user_id: UUID):
    for user in users:
        if str(user["id"]) == str(user_id):
            return {
                "data": user
            }
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )


# TODO:
@app.post("/user/signup", tags=["users"])
def user_signup(new_user: CreateUserSchema):
    # TODO: Check if user already exist
    # Check if user already exist
    for user in users:
        if user["email"] == new_user.email:
            raise HTTPException(status_code=400,
                                detail='Account with same Email already exist')
    if new_user.password != new_user.passwordConfirm:
        raise HTTPException(status_code=400,
                            detail='Passwords do not match')
    del new_user.passwordConfirm
    new_user.verified = True
    hashed_password = hash_password(new_user.password)
    user = {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "organization_name": new_user.organization_name,
        "email": new_user.email.lower(),
        "password": hashed_password,
        "created_at": datetime.utcnow(),
        "updated_at": None,
        "verified": True
    }
    # noinspection PyTypeChecker
    users.append(user)
    print(user)
    return sign_jwt(user["email"])


# This function checks and verify the user - if user with same email exists it will verify password
def check_user(data: UserLoginSchema):
    for user in users:
        if user["email"] == data.email and verify_password(data.password, user["password"]):
            return True
    return False


@app.post("/user/login", tags=["users"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return sign_jwt(user.email)
    return {
        "error": "Invalid login details!"
    }
