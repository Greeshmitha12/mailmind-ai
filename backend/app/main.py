from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database
import logging
from logging.handlers import RotatingFileHandler
import random
from fastapi_mail import FastMail, MessageSchema
from .email_config import conf
from sqlalchemy import func
from .scheduler import start_scheduler
from fastapi.responses import FileResponse
from .google_routes import router as google_router


# MailMind Tasks
from .mailmind_tasks import delete_expired_otps
from .calendar_tasks import create_event
from .drive_tasks import create_folder
from .mailmind_runner import run_mailmind

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("app.log", maxBytes=1000000, backupCount=3),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(google_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home Route
@app.get("/")
def root():
    return {
        "project": "MailMind",
        "status": "running"
    }

# Database Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

if conf:
    print("Mail Config Loaded")
else:
    print("Mail Disabled")
# Create User + Send OTP
@app.post("/users/")
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:

        if not existing_user.is_verified:

            otp = generate_otp()

            existing_user.otp = otp
            db.commit()

            message = MessageSchema(
                subject="MailMind OTP Verification",
                recipients=[user.email],
                body=f"Your OTP is: {otp}",
                subtype="plain"
            )

            fm = FastMail(conf)
            await fm.send_message(message)

            return {
                "status": "success",
                "message": "New OTP sent"
            }

        return {
            "status": "error",
            "message": "Email already registered and verified"
        }

    otp = generate_otp()

    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        otp=otp,
        is_verified=False,
        token_file=None
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    message = MessageSchema(
        subject="MailMind OTP Verification",
        recipients=[user.email],
        body=f"Your OTP is: {otp}",
        subtype="plain"
    )

    #fm = FastMail(conf)
    #await fm.send_message(message)

    print("OTP Email Sent")
    print("OTP:", otp)

    return {
        "id": db_user.id,
        "email": db_user.email,
        "message": "User created successfully. OTP sent to email."
    }

# Verify OTP
@app.post("/verify")
def verify_otp(
    data: schemas.VerifyOTP,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.email == data.email
    ).first()

    if not user:
        return {"message": "User not found"}

    if user.otp != data.otp:
        return {"message": "Invalid OTP"}

    user.is_verified = True
    user.otp = None

    db.commit()

    return {"message": "Email verified successfully"}

# Get Users
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Delete User
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if user:
        db.delete(user)
        db.commit()
        return {"message": "User deleted"}

    return {"error": "User not found"}

# Gmail OTP Cleanup
@app.post("/gmail/cleanup/{user_id}")
def cleanup_gmail(user_id: int):

    delete_expired_otps(user_id)

    return {
        "message": "OTP cleanup completed"
    }

# Calendar Event Creation
@app.post("/calendar/create-event/{user_id}")
def create_calendar_event(user_id: int):

    create_event(user_id=user_id)

    return {
        "message": "Calendar event created successfully"
    }

# Drive Folder Creation
@app.post("/drive/create-folder/{user_id}")
def create_drive_folder(user_id: int):

    create_folder(user_id)

    return {
        "message": "Drive folder created successfully"
    }
# Run Complete MailMind Workflow
@app.post("/mailmind/run/{user_id}")
def run_mailmind_workflow(user_id: int):

    run_mailmind(user_id)

    return {
        "message": "MailMind workflow completed successfully"
    }
@app.get("/mailmind/history/{user_id}")
def get_mailmind_history(
    user_id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        models.MailMindHistory
    ).filter(
        models.MailMindHistory.user_id == user_id
    ).all()
@app.get("/mailmind/stats")
def get_mailmind_stats(
    db: Session = Depends(get_db)
):

    total_runs = db.query(
        models.MailMindHistory
    ).count()

    total_events = db.query(
        func.sum(models.MailMindHistory.events_detected)
    ).scalar() or 0

    total_files = db.query(
        func.sum(models.MailMindHistory.files_uploaded)
    ).scalar() or 0

    total_otps = db.query(
        func.sum(models.MailMindHistory.otp_deleted)
    ).scalar() or 0

    return {
        "total_runs": total_runs,
        "total_events_detected": total_events,
        "total_files_uploaded": total_files,
        "total_otps_deleted": total_otps
    }
@app.on_event("startup")
async def startup_event():

    logger.info("MAILMIND SCHEDULER STARTED")
    start_scheduler()

@app.get("/mailmind/report")
def download_report():

    return FileResponse(
        path="mailmind_report.txt",
        filename="mailmind_report.txt",
        media_type="text/plain"
    )
@app.post("/resend-otp")
async def resend_otp(
    data: schemas.ResendOTP,
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.email == data.email
    ).first()

    if not user:
        return {
            "status": "error",
            "message": "User not found"
        }

    if user.is_verified:
        return {
            "status": "error",
            "message": "Email already verified"
        }

    otp = generate_otp()

    user.otp = otp
    db.commit()

    message = MessageSchema(
        subject="MailMind OTP Verification",
        recipients=[user.email],
        body=f"Your new OTP is: {otp}",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    return {
        "status": "success",
        "message": "New OTP sent"
    }   