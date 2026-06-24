from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_verified: bool
    token_file: str | None = None

    class Config:
        from_attributes = True


class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str


class GoogleConnectResponse(BaseModel):
    message: str
    user_id: int


class MailMindStatsResponse(BaseModel):
    total_runs: int
    total_events_detected: int
    total_files_uploaded: int
    total_otps_deleted: int