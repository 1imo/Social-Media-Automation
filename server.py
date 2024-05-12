import os
import shutil
from flask import Flask, render_template, jsonify, send_from_directory, request

from socials.socials_interface import SocialsInterface

app = Flask(__name__, static_folder="static", template_folder="templates")

# Directories
PENDING_APPROVAL = "./content/pending_approval"
APPROVED = "./content/approved"
os.makedirs(PENDING_APPROVAL, exist_ok=True)
os.makedirs(APPROVED, exist_ok=True)


# Response messages
SUCCESS = lambda message: (jsonify({"message": message}), 200)
ERROR = lambda error: (jsonify({"error": error}), 400)


# Interface
# Returns index.html from the templates folder
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Returns the list of videos in the pending approval folder
@app.route("/get_videos", methods=["GET"])
def get_videos():
    video_files = [f for f in os.listdir(PENDING_APPROVAL) if f.endswith(".mp4")]
    return jsonify(video_files)


# Serves the video file from the pending approval folder
@app.route("/videos/<filename>", methods=["GET"])
def serve_video(filename):
    return send_from_directory(PENDING_APPROVAL, filename)


# Deletes the video file from the pending approval folder
# Called on a scroll event
@app.route("/videos/<filename>", methods=["DELETE"])
def remove_video(filename):
    try:
        video_path = os.path.join(PENDING_APPROVAL, filename)
        os.remove(video_path)
        return SUCCESS("Video removed successfully")
    except Exception as e:
        return ERROR("Error removing video")


# Moves the video file to the approved folder
# Posts to specified platform
@app.route("/videos/<filename>", methods=["PUT"])
def move_video(filename):
    video_path = os.path.join(PENDING_APPROVAL, filename)
    new_video_path = os.path.join(APPROVED, filename)
    
    body = request.get_json()

    try:
        shutil.move(video_path, new_video_path)

        # TODO - CAPTION IMPLEMENTATION
        
        upload_interface.post_video(body.platform, new_video_path)
        
        return SUCCESS("Video uploaded successfully")
    except Exception as e:
        return ERROR("Error uploading video")


if __name__ == "__main__":
    upload_interface = SocialsInterface()
    
    app.run(debug=True)
