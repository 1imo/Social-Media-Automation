from socials.youtube import YouTube


class SocialsInterface:
    socials = ["youtube"]

    @staticmethod
    def post_video(self, video, platform):
        if platform not in self.socials:
            raise Exception("Invalid platform")

        if platform == "youtube":
            youtube.upload_short(video, "Title", "Description", None)


if __name__ == "__main__":
    youtube = YouTube()
