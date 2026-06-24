import re
from datetime import datetime, timedelta
from .google_auth import get_google_services


def delete_expired_otps(user_id):

    gmail_service, _, _ = get_google_services(user_id)

    results = gmail_service.users().messages().list(
        userId="me",
        q="newer_than:30d",
        maxResults=100
    ).execute()

    messages = results.get("messages", [])

    print("\n==============================")
    print("MAILMIND CLEANUP STARTED")
    print("==============================")

    deleted_count = 0

    otp_keywords = [
        "otp",
        "verification code",
        "one time password",
        "authentication code",
        "security code",
        "login code",
        "passcode",
        "verification pin",
        "your code"
    ]

    for msg in messages:

        try:

            msg_data = gmail_service.users().messages().get(
                userId="me",
                id=msg["id"]
            ).execute()

            snippet = msg_data.get(
                "snippet",
                ""
            ).lower()

            is_otp = any(
                keyword in snippet
                for keyword in otp_keywords
            )

            has_code = bool(
                re.search(r"\b\d{4,8}\b", snippet)
            )

            if is_otp or has_code:

                gmail_service.users().messages().trash(
                    userId="me",
                    id=msg["id"]
                ).execute()

                deleted_count += 1

                print(
                    f"Deleted OTP Email -> {msg['id']}"
                )

        except Exception as e:

            print(
                f"Cleanup Error -> {e}"
            )

    print(
        f"TOTAL EMAILS DELETED: {deleted_count}"
    )
    return {
        "otp_deleted": deleted_count
    }


def find_important_emails(user_id):

    gmail_service, _, _ = get_google_services(user_id)

    results = gmail_service.users().messages().list(
        userId="me",
        q="newer_than:30d",
        maxResults=50
    ).execute()

    messages = results.get("messages", [])

    important_keywords = [
        "interview",
        "meeting",
        "exam",
        "deadline",
        "appointment",
        "event",
        "webinar",
        "presentation",
        "hackathon"
    ]

    months = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12
    }

    print("\n==============================")
    print("SEARCHING IMPORTANT EMAILS")
    print("==============================")

    events = []

    for msg in messages:

        try:

            msg_data = gmail_service.users().messages().get(
                userId="me",
                id=msg["id"]
            ).execute()

            snippet = msg_data.get(
                "snippet",
                ""
            ).lower()

            headers = msg_data["payload"].get(
                "headers",
                []
            )

            subject = ""

            for header in headers:

                if header["name"].lower() == "subject":

                    subject = header["value"].lower()
                    break

            full_text = f"{subject} {snippet}"

            if not any(
                keyword in full_text
                for keyword in important_keywords
            ):
                continue

            print("\nIMPORTANT EMAIL FOUND")
            print("SUBJECT:", subject)

            event_hour = 10
            event_minute = 0

            # Detect Time
            time_match = re.search(
                r"(\d{1,2}):(\d{2})\s*(am|pm)",
                full_text,
                re.IGNORECASE
            )

            if time_match:

                event_hour = int(time_match.group(1))
                event_minute = int(time_match.group(2))

                am_pm = time_match.group(3).lower()

                if am_pm == "pm" and event_hour != 12:
                    event_hour += 12

                if am_pm == "am" and event_hour == 12:
                    event_hour = 0

                print(
                    f"DETECTED TIME: {event_hour}:{event_minute:02d}"
                )

            # Day Month
            match = re.search(
                r"(\d{1,2})(st|nd|rd|th)?\s+"
                r"(january|february|march|april|may|june|july|august|september|october|november|december)",
                full_text
            )

            if match:

                day = int(match.group(1))
                month_name = match.group(3)

                month = months[month_name]
                year = datetime.now().year

                start_time = datetime(
                    year,
                    month,
                    day,
                    event_hour,
                    event_minute
                )

                end_time = start_time + timedelta(hours=1)

                print(
                    f"DETECTED DATE: {day}-{month}-{year}"
                )

                events.append({
                    "title": subject.title(),
                    "start_time": start_time,
                    "end_time": end_time,
                    "location": "",
                    "meeting_link": ""
                })

                continue

            # Month Day Year
            match = re.search(
                r"(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2})(st|nd|rd|th)?\s+(\d{4})",
                full_text
            )

            if match:

                month_name = match.group(1)
                day = int(match.group(2))
                year = int(match.group(4))

                month = months[month_name]

                start_time = datetime(
                    year,
                    month,
                    day,
                    event_hour,
                    event_minute
                )

                end_time = start_time + timedelta(hours=1)

                print(
                    f"DETECTED DATE: {day}-{month}-{year}"
                )

                events.append({
                    "title": subject.title(),
                    "start_time": start_time,
                    "end_time": end_time
                })

                continue

            # Numeric Date
            match = re.search(
                r"(\d{1,2})[./-](\d{1,2})[./-](\d{4})",
                full_text
            )

            if match:

                day = int(match.group(1))
                month = int(match.group(2))
                year = int(match.group(3))

                start_time = datetime(
                    year,
                    month,
                    day,
                    event_hour,
                    event_minute
                )

                end_time = start_time + timedelta(hours=1)

                print(
                    f"DETECTED DATE: {day}-{month}-{year}"
                )

                events.append({
                    "title": subject.title(),
                    "start_time": start_time,
                    "end_time": end_time
                })

                continue

            print("\nNO DATE DETECTED")
            print("SUBJECT:", subject)

        except Exception as e:

            print(
                f"Email Processing Error: {e}"
            )

    print(f"\nTOTAL EVENTS FOUND: {len(events)}")

    return events