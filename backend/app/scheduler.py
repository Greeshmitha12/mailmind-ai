from apscheduler.schedulers.background import BackgroundScheduler

from .mailmind_runner import run_mailmind
from .database import SessionLocal
from .models import User


scheduler = BackgroundScheduler()


def run_all_users():

    db = SessionLocal()

    try:

        users = db.query(User).filter(
            User.is_verified == True
        ).all()

        print(
            f"\nRunning MailMind for {len(users)} users"
        )

        for user in users:

            try:

                print(
                    f"\nProcessing User ID: {user.id}"
                )

                run_mailmind(user.id)

            except Exception as e:

                print(
                    f"User {user.id} Error: {e}"
                )

    finally:

        db.close()


def start_scheduler():

    scheduler.add_job(
        run_all_users,
        "interval",
        minutes=5
    )

    scheduler.start()

    print("\n==============================")
    print("MAILMIND SCHEDULER STARTED")
    print("==============================")