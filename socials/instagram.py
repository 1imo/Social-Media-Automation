import requests
import os

# Set the API endpoint URLs
media_endpoint_url = (
    f"https://graph.facebook.com/v19.0/{os.environ.get(IG_PAGE_ID)}/video_reels"
)
video_upload_endpoint_url = (
    f"https://graph.facebook.com/v19.0/{os.environ.get(IG_PAGE_ID)}/video_reels"
)

# Set the access token
access_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")

# Set the path to your local video file
video_file_path = "../content/approved/C4C47TSOns_.mp4"

# Check if the video file exists
if not os.path.isfile(video_file_path):
    print("Video file not found.")
    exit(1)

# Step 1: Initialize an upload session
init_upload_params = {"upload_phase": "start", "access_token": access_token}
init_upload_response = requests.post(
    video_upload_endpoint_url, params=init_upload_params
)

if init_upload_response.status_code == 200:
    video_id = init_upload_response.json()["video_id"]
    upload_url = init_upload_response.json()["upload_url"]
    print("Upload session initialized. Video ID:", video_id)
else:
    print("Failed to initialize upload session.")
    print("Status code:", init_upload_response.status_code)
    print("Error message:", init_upload_response.json().get("error", {}).get("message"))
    exit(1)

# Step 2: Upload the video file
with open(video_file_path, "rb") as video_file:
    video_data = video_file.read()
    video_upload_headers = {
        "Authorization": f"OAuth {access_token}",
        "offset": "0",
        "file_size": str(os.path.getsize(video_file_path)),
    }
    video_upload_response = requests.post(
        upload_url, headers=video_upload_headers, data=video_data
    )

    if video_upload_response.status_code == 200:
        print("Video uploaded successfully.")
    else:
        print("Failed to upload video.")
        print("Status code:", video_upload_response.status_code)
        print(
            "Error message:",
            video_upload_response.json().get("error", {}).get("message"),
        )
        exit(1)

# Step 3: Publish the reel
publish_reel_params = {
    "access_token": access_token,
    "video_id": video_id,
    "upload_phase": "finish",
    "video_state": "PUBLISHED",
    "description": "Check out this amazing reel! #awesome",
}
publish_reel_response = requests.post(media_endpoint_url, params=publish_reel_params)

if publish_reel_response.status_code == 200:
    print("Reel published successfully!")
else:
    print("Failed to publish reel.")
    print("Status code:", publish_reel_response.status_code)
    print(
        "Error message:", publish_reel_response.json().get("error", {}).get("message")
    )
