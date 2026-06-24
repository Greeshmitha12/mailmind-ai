from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    otp = Column(
        String,
        nullable=True
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    token_file = Column(
        String,
        nullable=True
    )


class MailMindHistory(Base):
    __tablename__ = "mailmind_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    run_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    otp_deleted = Column(
        Integer,
        default=0
    )

    events_detected = Column(
        Integer,
        default=0
    )

    files_uploaded = Column(
        Integer,
        default=0
    )
