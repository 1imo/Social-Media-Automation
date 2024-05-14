import os
import time
from collections import deque
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from socials.socials_interface import SocialsInterface
from libs.singleton import Singleton
from data.instagram import Instagram


# Watch folders for cleaner content management
# Manages pending and approved directories
# New videos are posted through the socials_interface
# New videos are fetched if there are less than 2 in the pending directory
# Can be adjusted if it takes too long between fetching content and scrolling/watching through the UI
# One instance to preserve state and no more is needed anyway
class FolderEvents(PatternMatchingEventHandler, metaclass=Singleton):
    patterns = ["*.mp4"]
    APPROVED_DIR = "../content/approved"
    PENDING_DIR = "../content/pending_approval"

    def __init__(self):
        super().__init__()
        # Check the amount of pending videos on init
        self.pending_left = self.count_pending_videos()
        if self.pending_left < 2:
            # Fetch content if there are less than 2 pending videos
            self.on_deleted(None)

    # Count the amount of pending videos
    def count_pending_videos(self):
        return sum(
            1
            for file in os.listdir(self.PENDING_DIR)
            if os.path.isfile(os.path.join(self.PENDING_DIR, file))
            and os.path.splitext(file)[1].lower() in self.video_extensions
        )

    # If new video file in the approved directory, post it
    def on_created(self, event):
        file_path = os.path.join(event.src_path, event.src_path.split(os.sep)[-1])
        self.last_created_file = file_path
        if event.src_path == self.APPROVED_DIR:
            SocialsInterface.post_video(file_path, "youtube")

    # If video file is deleted from the pending directory
    # Fetch content if there are less than 2 pending videos
    def on_deleted(self, event):
        if event is None or event.src_path == self.PENDING_DIR:
            self.pending_left -= 1
            if self.pending_left < 2:
                Instagram.fetch_content()
                self.pending_left = self.count_pending_videos()

    # Start watching the directories
    def start_watching(self):
        observer = Observer()
        observer.schedule(self, self.APPROVED_DIR, recursive=False)
        observer.schedule(self, self.PENDING_DIR, recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()


# Example usage
if __name__ == "__main__":
    folder_events = FolderEvents()
    folder_events.start_watching()
