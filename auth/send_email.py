import smtplib
import os
import math
import random
import ssl
from email.message import EmailMessage

def OTP_GOGGLE(input_email="example@gmail.com"):
    digits="0123456789"
    OTP=""
    for i in range(6):
        OTP+=digits[math.floor(random.random()*10)]

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "avcjasamarga@gmail.com"
    receiver_email = input_email
    password = "mitptrudyexcfskm"
    
    em=EmailMessage()
    em['From']=sender_email
    em['To']=input_email
    em['subject']="AUTHORIZED LOGIN"
    body="HERE IS YOUR OTP CODE "+str(OTP)
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, em.as_string())

    print("berhasil")
    json_otp={"otp":OTP}

    return json_otp

