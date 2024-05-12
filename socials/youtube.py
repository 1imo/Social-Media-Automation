from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class GoogleAuth:
    def __init__(self, client_secret_file, scopes, redirect_uri):
        self.flow = InstalledAppFlow.from_client_secrets_file(
            client_secret_file, scopes, redirect_uri=redirect_uri
        )

    def get_credentials(self):
        return self.flow.run_local_server(port=0)

class YouTube:
    def __init__(self):
        client_secret_file = "../config/client_secret_293899501274acd1.json"
        scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        redirect_uri = "http://localhost"
        
        auth = GoogleAuth(client_secret_file, scopes, redirect_uri)
        credentials = auth.get_credentials()
        
        self.youtube = build("youtube", "v3", credentials=credentials)
        
    
    def upload_short(self, video_file, title, description, credentials):
        uploader = self.youtube

        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": "22",
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        }

        media_file = MediaFileUpload(video_file, chunksize=-1, resumable=True)

        request = uploader.youtube.videos().insert(
            part="snippet,status", body=request_body, media_body=media_file
        )

        response = request.execute()
        print(f'Video ID: {response["id"]}')