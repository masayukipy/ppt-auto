from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("credentials")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("credentials")
drive = GoogleDrive(gauth)


class Drive:
    def __init__(self) -> None:
        pass

    def upload_file(self, driver_id: str, local_path: str):
        file_name = local_path.split("/")[-1]
        file_name = file_name.split("\\")[-1]
        file = drive.CreateFile({"title": file_name, "parents": [{"id": driver_id}]})
        file.SetContentFile(local_path)
        file.Upload()
        return file["id"]

    def create_driver_directory(self, directory_name: str, parent_id="root"):
        file_metadata = {
            "title": directory_name,
            # "parents": [{"id": parent_id}],
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_id != "root":
            file_metadata["parents"] = [{"id": parent_id}]
        folder = drive.CreateFile(file_metadata)
        folder.Upload()
        return folder["id"]
