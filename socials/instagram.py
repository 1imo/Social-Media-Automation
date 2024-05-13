# libs = os.path("../__init__.py")
from account_management import Firefox
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD
from instaloader import Profile, Instaloader, Post
import os


class Instagram:
    PENDING_APPROVAL_DIR: str = "../content/pending_approval"

    def __init__(self) -> None:
        print("Initializing Instagram class...")
        firefox = Firefox()
        # self.instaloader: Instaloader = firefox.login(
        #     INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD
        # )
        self.instaloader: Instaloader = firefox.get_session()
        self.context = self.instaloader.context

    def get_user(self, username: str) -> Profile:
        print(f"Getting user: {username}")
        return Profile.from_username(self.context, username)

    def get_similar_profiles(self, profile: Profile) -> list[Profile]:
        print("Getting similar profiles...")
        return list(Profile.get_similar_accounts(profile))

    def get_feed(self) -> list[Post]:
        print("Getting feed posts...")
        return list(Instaloader.get_feed_posts(self.context))

    def get_saved_posts(self) -> list[Post]:
        print("Getting saved posts...")
        return list(Profile.get_saved_posts(self.context))

    def get_users_posts(self, profile: Profile) -> list[Post]:
        print("Getting user's posts...")
        return list(Profile.get_posts(profile))

    def get_explore_posts(self) -> list[Post]:
        print("Getting explore posts...")
        return list(Instaloader.get_explore_posts(self.context))

    def save_post(self, post: Post) -> None:
        print("Saving post...")
        os.makedirs(self.PENDING_APPROVAL_DIR, exist_ok=True)

        if post.is_video:
            video_filename: str = f"{post.shortcode}.mp4"
            self.instaloader.download_post(post, target=self.PENDING_APPROVAL_DIR)
            os.rename(
                os.path.join(self.PENDING_APPROVAL_DIR, post.video_filename),
                os.path.join(self.PENDING_APPROVAL_DIR, video_filename),
            )
            print(f"Renamed video to {video_filename}")
