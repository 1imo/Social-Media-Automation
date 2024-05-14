# libs = os.path("../__init__.py")
from account_management import Firefox
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD
from instaloader import Profile, Instaloader, Post
import os
from libs.singleton import Singleton


# Fetch content from Instagram (video)
# Singular instance across the codebase
class Instagram(metaclass=Singleton):
    PENDING_APPROVAL_DIR: str = "../content/pending_approval"

    def __init__(self) -> None:
        print("Initializing Instagram class...")
        firefox = Firefox()

        # I think IG is blocking the login which allows for better scraping thorugh similar accounts and feed.
        # So annoyed, I'll try again later
        # self.instaloader: Instaloader = firefox.login(
        #     INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD
        # )
        self.instaloader: Instaloader = firefox.get_session()
        self.context = self.instaloader.context

    # Only available on a login which wasn't working last time I checked
    def get_similar_profiles(self, profile: Profile) -> list[Profile]:
        print("Getting similar profiles...")
        return list(Profile.get_similar_accounts(profile))

    # Login too
    def get_feed(self) -> list[Post]:
        print("Getting feed posts...")
        return list(Instaloader.get_feed_posts(self.context))

    # Also login
    def get_saved_posts(self) -> list[Post]:
        print("Getting saved posts...")
        return list(Profile.get_saved_posts(self.context))

    # Get a user's posts
    def get_users_posts(self, profile: Profile) -> list[Post]:
        print("Getting user's posts...")
        return list(Profile.get_posts(profile))

    def get_explore_posts(self) -> list[Post]:
        print("Getting explore posts...")
        return list(Instaloader.get_explore_posts(self.context))

    @staticmethod
    def fetch_content(self) -> None:
        posts = self.get_explore_posts()
        for post in posts:
            self.save_post(post)

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
