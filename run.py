import sys
import os

parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)


from socials.instagram import Instagram


if __name__ == "__main__":
    # instagram = Instagram()
    # print(instagram)

    # user = instagram.get_user("zumzoooom")
    # # print(instagram.get_similar_profiles(user))
    # # print(instagram.get_feed())
    # # Convert the iterator to a list
    # user_posts = instagram.get_users_posts(user)
    # print(len(user_posts), "posts found.")
    # # print(instagram.get_explore_posts())
    # # Save the first post
    # # if user_posts:
    # #     instagram.save_post(user_posts[0])
    # # else:
    # #     print("No posts found for the user.")

    from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

    from pygramcore import Account

    Account.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    print("LOGGED IN")
    Account.save_cookies("./file.pkl")
    Account.load_cookies("./file.pkl")
    print("COOKIES LOADED")

    Account.post("./content/pending_approval/C4C47TSOns_.mp4", "#cars")
    print("POSTED")
