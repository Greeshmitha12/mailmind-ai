import os
import base64

from .google_auth import get_google_services


def upload_email_attachments(user_id):

    gmail_service, _, drive_service = get_google_services(user_id)

    folder_result = drive_service.files().list(
        q="name='MailMind Files' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id,name)"
    ).execute()

    folders = folder_result.get(
        "files",
        []
    )

    if not folders:

        print("MailMind Files folder not found")
        return 0

    folder_id = folders[0]["id"]

    print("\nUsing Folder ID:", folder_id)

    results = gmail_service.users().messages().list(
        userId="me",
        q="has:attachment newer_than:30d",
        maxResults=50
    ).execute()

    messages = results.get(
        "messages",
        []
    )

    print("\n==============================")
    print("ATTACHMENT SCAN STARTED")
    print("==============================")

    upload_count = 0

    for msg in messages:

        try:

            message = gmail_service.users().messages().get(
                userId="me",
                id=msg["id"]
            ).execute()

            payload = message.get(
                "payload",
                {}
            )

            parts = payload.get(
                "parts",
                []
            )

            for part in parts:

                filename = part.get(
                    "filename",
                    ""
                )

                if not filename:
                    continue

                allowed_extensions = (
                    ".pdf",
                    ".doc",
                    ".docx",
                    ".ppt",
                    ".pptx",
                    ".xls",
                    ".xlsx"
                )

                if not filename.lower().endswith(
                    allowed_extensions
                ):
                    continue

                existing_files = drive_service.files().list(
                    q=(
                        f"name='{filename}' and "
                        f"'{folder_id}' in parents and "
                        f"trashed=false"
                    ),
                    fields="files(id,name)"
                ).execute()

                if existing_files.get("files"):

                    print(
                        f"FILE ALREADY EXISTS -> {filename}"
                    )

                    continue

                attachment_id = (
                    part.get(
                        "body",
                        {}
                    ).get(
                        "attachmentId"
                    )
                )

                if not attachment_id:
                    continue

                attachment = (
                    gmail_service.users()
                    .messages()
                    .attachments()
                    .get(
                        userId="me",
                        messageId=msg["id"],
                        id=attachment_id
                    )
                    .execute()
                )

                file_data = base64.urlsafe_b64decode(
                    attachment["data"]
                )

                os.makedirs(
                    "downloads",
                    exist_ok=True
                )

                temp_path = os.path.join(
                    "downloads",
                    filename
                )

                with open(
                    temp_path,
                    "wb"
                ) as f:

                    f.write(file_data)

                file_metadata = {
                    "name": filename,
                    "parents": [folder_id]
                }

                uploaded_file = (
                    drive_service.files()
                    .create(
                        body=file_metadata,
                        media_body=temp_path,
                        fields="id,name"
                    )
                    .execute()
                )

                upload_count += 1

                print(
                    f"Uploaded: {filename}"
                )

                print(
                    f"Drive File ID: {uploaded_file['id']}"
                )

        except Exception as e:

            print(
                f"Attachment Error: {e}"
            )

    print("\n==============================")
    print("ATTACHMENT SCAN COMPLETED")
    print(
        f"TOTAL FILES UPLOADED: {upload_count}"
    )
    print("==============================")

    return upload_count