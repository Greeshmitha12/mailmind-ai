from .mailmind_tasks import (
    delete_expired_otps,
    find_important_emails
)

from .calendar_tasks import create_event
from .drive_tasks import create_folder
from .report_tasks import generate_report
from .history_tasks import save_history

try:
    from .attachment_tasks import upload_email_attachments
except Exception:
    def upload_email_attachments(user_id):
        return 0


def run_mailmind(user_id):

    print("\n==============================")
    print("MAILMIND WORKFLOW STARTED")
    print("==============================")

    otp_result = delete_expired_otps(user_id)

    if isinstance(otp_result, dict):
        deleted_otps = otp_result.get(
            "otp_deleted",
            0
        )
    else:
        deleted_otps = otp_result

    events = find_important_emails(user_id)

    total_events = len(events)

    print("\n==============================")
    print(f"TOTAL EVENTS DETECTED: {total_events}")
    print("==============================")

    for event in events:

        create_event(
            user_id=user_id,
            title=event["title"],
            start_time=event["start_time"],
            end_time=event["end_time"],
            location=event.get(
                "location",
                ""
            )
        )

    create_folder(user_id)

    uploaded_files = upload_email_attachments(
        user_id
    )

    report_file = generate_report(
        deleted_otps,
        total_events,
        uploaded_files
    )

    print("REPORT FILE:", report_file)

    save_history(
        user_id,
        deleted_otps,
        total_events,
        uploaded_files
    )

    print("\n==============================")
    print("MAILMIND WORKFLOW COMPLETED")
    print("==============================")