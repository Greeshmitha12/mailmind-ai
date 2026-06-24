from datetime import datetime, timedelta
from .google_auth import get_google_services


def create_event(
    user_id,
    title="MailMind Event",
    start_time=None,
    end_time=None,
    location="",
    description="Automatically created by MailMind"
):

    try:

        _, calendar_service, _ = get_google_services(user_id)

        if start_time is None:
            start_time = datetime.now() + timedelta(minutes=5)

        if end_time is None:
            end_time = start_time + timedelta(hours=1)

        events_result = calendar_service.events().list(
            calendarId="primary",
            maxResults=250,
            singleEvents=True
        ).execute()

        events = events_result.get("items", [])

        for existing_event in events:

            existing_title = existing_event.get(
                "summary",
                ""
            )

            existing_start = (
                existing_event.get(
                    "start",
                    {}
                ).get(
                    "dateTime",
                    ""
                )
            )

            if existing_title.lower() != title.lower():
                continue

            if str(start_time.date()) in existing_start:

                print("\n==============================")
                print("EVENT ALREADY EXISTS")
                print("==============================")
                print("Title:", title)
                print("Start:", start_time)
                print("==============================\n")

                return None

        event = {
            "summary": title,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "Asia/Kolkata"
            }
        }

        created_event = calendar_service.events().insert(
            calendarId="primary",
            body=event
        ).execute()

        print("\n==============================")
        print("CALENDAR EVENT CREATED")
        print("==============================")
        print("Title:", title)
        print("Start:", start_time)
        print("End:", end_time)
        print(created_event["htmlLink"])
        print("==============================\n")

        return created_event["htmlLink"]

    except Exception as e:

        print(f"Calendar Error: {e}")

        return None