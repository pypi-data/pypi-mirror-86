import os
import io
from googleapiclient import discovery, http, errors
from google.oauth2 import service_account

from .config import mimetypes

__version__ = "0.0.2"


class Client(object):

    service = None

    def __init__(self, **kwargs):
        credential_path = kwargs.get("credential_path") or os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )

        if credential_path is None:
            raise Exception("Please set GOOGLE_APPLICATION_CREDENTIALS")

        if not os.path.isfile(credential_path):
            raise Exception("Credential file path is not exists")

        credentials = service_account.Credentials.from_service_account_file(
            credential_path,
            scopes=[
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/drive.file",
            ],
        )

        self.service = discovery.build("drive", "v3", credentials=credentials)

    def list_folders(self, parent_id: str = None, **kwargs) -> dict:
        """
        List all folders in Google Drive folder

        Args:
            parent_id (str, optional): Parent folder id. Defaults to None.

        Returns:
            dict: List request result
        """

        parent_q = f"and '{parent_id}' in parents" if parent_id else ""

        q = f"mimeType = '{mimetypes['folder']}' {parent_q}"
        if kwargs.get("q"):
            q = f"{q} and {kwargs.get('q', '')}"

        result = (
            self.service.files()
            .list(
                **self.__list_parameter(
                    q=q,
                    page_size=kwargs.get("page_size", 1000),
                    next_page_token=kwargs.get("next_page_token"),
                    drive_id=kwargs.get("drive_id"),
                ),
            )
            .execute()
        )

        folders = result.get("files", [])

        next_page_token = result.get("nextPageToken")
        if next_page_token is not None and kwargs.get("fetch_all", False):
            res = self.list_folder(
                parent_id, fetch_all=True, next_page_token=next_page_token
            )
            folders += res["items"]
            next_page_token = res["next_page_token"]

        return {"items": folders, "next_page_token": next_page_token}

    def list_files(self, parent_id: str = None, **kwargs) -> dict:
        """
        List all files in Google Drive folder

        Args:
            parent_id (str, optional): Parent folder id. Defaults to None.

        Returns:
            dict: List request result
        """

        parent_q = f"and '{parent_id}' in parents" if parent_id else ""

        q = f"mimeType != '{mimetypes['folder']}' {parent_q}"
        if kwargs.get("q"):
            q = f"{q} and {kwargs.get('q', '')}"

        result = (
            self.service.files()
            .list(
                **self.__list_parameter(
                    q=q,
                    page_size=kwargs.get("page_size", 1000),
                    next_page_token=kwargs.get("next_page_token"),
                    drive_id=kwargs.get("drive_id"),
                ),
            )
            .execute()
        )

        files = result.get("files", [])

        next_page_token = result.get("nextPageToken")
        if next_page_token is not None and kwargs.get("fetch_all", False):
            res = self.list_folder(
                parent_id, fetch_all=True, next_page_token=next_page_token
            )

            files += res["items"]
            next_page_token = res["next_page_token"]

        return {"items": files, "next_page_token": next_page_token}

    def __list_parameter(self, **kwargs) -> dict:
        param = {
            "q": kwargs.get("q"),
            "pageSize": kwargs.get("page_size", 1000),
            "pageToken": kwargs.get("next_page_token"),
            "includeItemsFromAllDrives": True,
            "supportsAllDrives": True,
        }

        if kwargs.get("drive_id"):
            param["corpora"] = "drive"
            param["driveId"] = kwargs.get("drive_id")

        return param

    def get(self, file_id: str) -> dict:
        """
        Get Google Drive file info by file id

        Args:
            file_id (str): Google Drive file id

        Returns:
            dict: GET request result
        """

        try:
            return (
                self.service.files()
                .get(
                    fileId=file_id,
                )
                .execute()
            )

        except errors.HttpError as e:
            # file id not found
            return None

    def download(self, file_id: str, **kwargs) -> str:
        """
        Download Google Drive file by file id

        Args:
            file_id (str): Google Drive file id

        Raises:
            Exception: file not found

        Returns:
            str: file path
        """

        file = self.get(file_id)

        if not file:
            # todo exception refaction
            raise Exception("File is not exists")

        request = self.service.files().get_media(
            fileId=file_id,
        )

        fh = io.BytesIO()
        downloader = http.MediaIoBaseDownload(fh, request)

        done = False
        while done is False:
            status, done = downloader.next_chunk()

        folder = kwargs.get("folder", "")
        folder = folder if folder.endswith("/") or len(folder) == 0 else f"{folder}/"

        file_path = f"{folder}{file['name']}"

        # Write the stuff
        with open(file_path, "wb") as f:
            f.write(fh.getbuffer())

        return file_path

    def create_folder(self, parent_id: str = None, **kwargs) -> dict:
        """
        Create Google Dirve folder

        Args:
            parent_id (str, optional): Parent folder id. Defaults to None.

        Returns:
            dict: Create request result
        """

        body = {
            "name": kwargs.get("name", ""),
            "mimeType": config.mimetypes["folder"],
        }

        if parent_id:
            body["parents"] = [parent_id]

        return self.service.files().create(body=body).execute()

    def upload(self, parent_id: str = None, **kwargs) -> dict:
        """
        Upload file to Google drive

        Args:
            parent_id (str, optional): File parent folder. Defaults to None.

        Returns:
            dict: Upload request result
        """

        body = {"name": kwargs.get("filename")}

        if parent_id:
            body["parents"] = [parent_id]

        result = (
            self.service.files()
            .create(
                body=body,
                media_body=discovery.MediaFileUpload(kwargs.get("file_path")),
                supportsAllDrives=True,
            )
            .execute()
        )

        return result

    def delete(self, file_id: str) -> bool:
        """
        Delete google drive file

        Args:
            file_id (str): Google Drive file id

        Returns:
            bool: delete success or fail
        """

        try:
            self.service.files().delete(
                fileId=file_id, supportsAllDrives=True
            ).execute()

            return True

        except errors.HttpError as e:
            # print(e.resp.status)
            # 403 (don't have permission to delete)
            # 404 (file id not found)

            return False

    def list_permissions(self, file_id: str) -> dict:
        """
        List Google Drive file permissions by file id

        Args:
            file_id (str): Google Drive file id

        Returns:
            dict: List request result
        """

        try:
            return self.service.permissions().list(fileId=file_id).execute()

        except errors.HttpError as e:
            return None

    def create_permission(self, file_id: str, role: str, email: str) -> dict:
        """
        Create share permission for file

        Args:
            file_id (str): Google Drive file id
            role (str): Share role
            email (str): Share user email

        Raises:
            Exception: Role not support

        Returns:
            dict: Create request result
        """

        if role not in [
            "owner",
            "organizer",
            "fileOrganizer",
            "writer",
            "commenter",
            "reader",
        ]:
            raise Exception(f"Role: {role} is not support")

        result = (
            self.service.permissions()
            .create(
                fileId=file_id,
                body={"role": role, "type": "user", "emailAddress": email},
            )
            .execute()
        )

        return result

    def about(self) -> dict:
        """
        Show Google Drive info by credential user

        Returns:
            dict: Get request result
        """

        return self.service.about().get(fields="*").execute()
