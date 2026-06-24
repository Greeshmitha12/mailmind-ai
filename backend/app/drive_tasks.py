from .google_auth import get_google_services


def create_folder(user_id):

    try:

        _, _, drive_service = get_google_services(user_id)

        results = drive_service.files().list(
            q="name='MailMind Files' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            fields="files(id,name,webViewLink)"
        ).execute()

        folders = results.get("files", [])

        if folders:

            folder = folders[0]

            print("\n==============================")
            print("DRIVE FOLDER ALREADY EXISTS")
            print("==============================")
            print("Folder Name:", folder["name"])
            print("Folder ID:", folder["id"])

            return folder

        folder_metadata = {
            "name": "MailMind Files",
            "mimeType": "application/vnd.google-apps.folder"
        }

        folder = drive_service.files().create(
            body=folder_metadata,
            fields="id,name,webViewLink"
        ).execute()

        print("\n==============================")
        print("DRIVE FOLDER CREATED")
        print("==============================")
        print("Folder Name:", folder["name"])
        print("Folder ID:", folder["id"])

        return folder

    except Exception as e:

        print(f"Drive Error: {e}")

        return None