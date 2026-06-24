from datetime import datetime


def generate_report(
    deleted_otps,
    total_events,
    uploaded_files
):

    report = f"""
==============================
MAILMIND DAILY REPORT
==============================

Generated On:
{datetime.now()}

OTP Emails Deleted:
{deleted_otps}

Important Events Detected:
{total_events}

Attachments Uploaded:
{uploaded_files}

==============================
END OF REPORT
==============================
"""

    with open(
        "mailmind_report.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

    print("\n==============================")
    print("REPORT GENERATED")
    print("==============================")

    return "mailmind_report.txt"