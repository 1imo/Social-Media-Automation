import os
import time
from collections import deque
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from socials.socials_interface import SocialsInterface


# Watches folder events to fetch more content and manages upload calls
# I know this isn't really programming to interface but it's an exception
# NOT READY AND A MESS RN
class FolderEvents(PatternMatchingEventHandler):
    patterns = ["*.mp4"]

    def __init__(self):
        super().__init__()

    def on_created(self, event):
        file_path = os.path.join(event.src_path, event.src_path.split(os.sep)[-1])
        self.last_created_file = file_path
        SocialsInterface.post_video(file_path, "youtube")

    def on_deleted(self, event):
        file_path = os.path.join(event.src_path, event.src_path.split(os.sep)[-1])


if __name__ == "__main__":
    APPROVED_DIR = "../content/approved"
    PENDING_DIR = "../content/pending_approval"

    event_handler = FolderEvents()
    observer = Observer()
    observer.schedule(event_handler, APPROVED_DIR, recursive=False)
    observer.schedule(event_handler, PENDING_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
