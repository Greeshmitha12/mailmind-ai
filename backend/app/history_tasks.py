from .database import SessionLocal
from .models import MailMindHistory


def save_history(
    user_id,
    otp_deleted,
    events_detected,
    files_uploaded
):

    db = SessionLocal()

    try:

        history = MailMindHistory(
            user_id=user_id,
            otp_deleted=otp_deleted,
            events_detected=events_detected,
            files_uploaded=files_uploaded
        )

        db.add(history)
        db.commit()

        print("\n==============================")
        print("HISTORY SAVED")
        print("==============================")

    except Exception as e:

        print(f"History Error: {e}")

    finally:

        db.close()