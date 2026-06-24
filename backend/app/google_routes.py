from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
import os

from .database import SessionLocal
from .models import User

router = APIRouter()

oauth_flows = {}

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive"
]

CLIENT_FILE = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "credentials.json"
    )
)

REDIRECT_URI = "http://127.0.0.1:8000/google/callback"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/google/login/{user_id}")
def google_login(user_id: int):

    flow = Flow.from_client_secrets_file(
        CLIENT_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    oauth_flows[state] = {
        "flow": flow,
        "user_id": user_id
    }

    return RedirectResponse(auth_url)


@router.get("/google/callback")
def google_callback(
    state: str,
    code: str,
    db: Session = Depends(get_db)
):

    oauth_data = oauth_flows.get(state)

    if not oauth_data:
        raise HTTPException(
            status_code=400,
            detail="OAuth session expired. Start login again."
        )

    flow = oauth_data["flow"]
    user_id = oauth_data["user_id"]

    flow.fetch_token(code=code)

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    creds = flow.credentials

    token_file = f"token_{user_id}.json"

    with open(token_file, "w") as token:
        token.write(creds.to_json())

    user.token_file = token_file
    db.commit()

    oauth_flows.pop(state, None)

    return {
        "message": "Google connected successfully",
        "token_file": token_file
    }