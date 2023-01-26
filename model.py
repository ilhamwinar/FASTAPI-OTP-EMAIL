import uvicorn
from pydantic import BaseModel, Field,EmailStr

class PostSchema(BaseModel):
    id: int=Field(default=None)
    title: str= Field(default=None)
    content : str= Field(default=None)
    class Config:
        schema_extra={
            "post_demo":{
                "title":"some title about animal",
                "content":"some content",
            }
        }

class UserSchema(BaseModel):
    fullname : str = Field(default=None)
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)

    class config:
        the_schema = {
            "user_demo":{
                "name": "Bek",
                "email": "help@bekbrace.com",
                "password":"123"
            }
        }

class UserLoginSchema(BaseModel):
    #fullname : str = Field(default=None)
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)
#"name": "Bek",
    class config:
        the_schema = {
            "user_demo":{
                "email": "help@bekbrace.com",
                "password":"123"
            }
        }

class UserOTPSchema(BaseModel):
    otp : str = Field(default=None)
    class config:
        the_schema = {
            "user_demo":{
                "otp": "otp code",
            }
        }
