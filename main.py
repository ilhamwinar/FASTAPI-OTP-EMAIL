import uvicorn
from fastapi import FastAPI, Body, Depends, HTTPException
from model import PostSchema,UserLoginSchema,UserSchema,UserOTPSchema
from auth.jwt_handler import signJWT,otpJWT
from auth.jwt_bearer import JWTBearer
from auth.send_email import OTP_GOGGLE
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from passlib.context import CryptContext
import mysql.connector
import logging

import smtplib
import os
import math
import random
import ssl
from email.message import EmailMessage


origins = ["*"]

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

posts = [
    {
        "id":1,
        "title":"penguin",
        "text":"penguin is animal"
    },
    {
        "id":2,
        "title":"tiger",
        "text":"tiger 1 is animal"
    },
    {
        "id":3,
        "title":"koala",
        "text":"koalas 1 is animal"
    },
]

users = []


@app.get("/")
def greet():
    return {"hello":"world"}

#get posts
@app.get("/posts",tags=["posts"])
def get_post():
    return {"data":posts}

@app.get("/posts/{id}",tags=["posts"])
def get_one_post(id:int):
    if id>len(posts):
        return { "error":"post with this ID does not exist"}
    for post in posts:
        if post['id']==id:
            return{
                "data":post
            }

@app.post("/posts",dependencies=[Depends(JWTBearer())], tags=["posts"])
def add_post(post:PostSchema):
    post.id=len(posts)+1
    posts.append(post.dict())
    return{"info":"post Added"}

# def OTP_GOGGLE(input_email):
#     digits="0123456789"
#     OTP=""
#     for i in range(6):
#         OTP+=digits[math.floor(random.random()*10)]

#     port = 587  # For starttls
#     smtp_server = "smtp.gmail.com"
#     sender_email = "avcjasamarga@gmail.com"
#     receiver_email = input_email
#     password = "mitptrudyexcfskm"
    
#     em=EmailMessage()
#     em['From']=sender_email
#     em['To']=input_email
#     em['subject']="AUTHORIZED LOGIN"
#     body="HERE IS YOUR OTP CODE "+str(OTP)
#     em.set_content(body)

#     context = ssl.create_default_context()
#     with smtplib.SMTP(smtp_server, port) as server:
#         server.ehlo()  # Can be omitted
#         server.starttls(context=context)
#         server.ehlo()  # Can be omitted
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, em.as_string())

#     print("berhasil")

#     return {"otp":OTP}

#usersignup
@app.post("/user/signup",tags=["user"])
async def user_signup(user: UserSchema=Body(default=None)):
    global result_otp
    # print(user.email)
    result_otp = OTP_GOGGLE(str(user.email))
    print(result_otp)
    users.append(user)
    result_otp.update(otpJWT(user.email))
    print(result_otp)
    return result_otp

@app.post("/user/otp",dependencies=[Depends(JWTBearer())],tags=["user"])
async def user_otp(user: UserOTPSchema=Body(default=None)):
    #print(otp_send)
    print("result post: "+user.otp)
    print(type(user.otp))
    if result_otp['otp'] == user.otp:
        print("berhasil")
    else:
        print("failed")
    return{"info":"success"}

#cek user apakah exist?

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email==data.email and user.password == data.password:
            return True
        else:
            return False

@app.post("/user/login",tags=["user"])
def user_login(user: UserLoginSchema=Body(default=None)):
    if check_user(user):
        print(result_otp)
        return signJWT(user.email)
    else:
        return{ "error":"invalid login details!"}

if __name__ == "__main__":
    #uvicorn.run("main:app", host="192.168.0.117", port=90,log_level="info",reload=True)
    uvicorn.run("main:app", host="192.168.68.75", port=90,log_level="info",reload=True)