from pydantic_django import ModelSchema
from blog.models import Article

# Django Ninja
from datetime import datetime
from ninja import Schema


# Pydantic Django
class ArticleSchema(ModelSchema):
    class Config:
        model = Article
# Pydantic Django
class ArticleResponseSchema(ModelSchema):
    class Config:
        model = Article
        exclude = ['created']

# Django Ninja
class UserSchema(Schema):
    id: int
    username: str

class ArticleIn(Schema):
    author: int
    title: str
    content: str

class ArticleOut(Schema):
    id: int
    author: UserSchema
    created: datetime
    title: str
    content: str
