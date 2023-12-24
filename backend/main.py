from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from typing import List, Dict, Any
import os
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

templates = Jinja2Templates(directory="./templates")

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this based on your deployment needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# class EmailSchema(BaseModel):
#     email: List[EmailStr]


class EmailContent(BaseModel):
    # subject: str
    # body: Dict[str, Any]

    form_data: Dict[str, Any]


email = ["vbvijay84@gmail.com"]
conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
    MAIL_FROM=os.environ.get("MAIL_USERNAME"),
    MAIL_PORT=os.environ.get("MAIL_PORT"),
    MAIL_SERVER=os.environ.get("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER="./templates",
)


@app.post("/send/email", response_class=HTMLResponse)
async def send_email(content: EmailContent, background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject="New Contact",
        recipients=email,
        template_body=content.dict().get("form_data"),
        subtype=MessageType.html,
        # form_data=content.form_data,
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message, template_name="email.html")
    return JSONResponse(
        status_code=200, content={"message": "Email will be sent in the background"}
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}
