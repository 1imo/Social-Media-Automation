import glob
import os
import shutil
import sqlite3
from instaloader import ConnectionException, Instaloader


# Fetch cookies from Firefox, test login, return session
class Firefox:
    SESSION_DIR = "../config"
    SESSION = f"{SESSION_DIR}/session.file"

    instaloader = Instaloader(max_connection_attempts=1)

    def login(self, username, password):
        print("Logging in...")
        self.instaloader.login(username, password)
        return self.instaloader

    @staticmethod
    def get_cookiefile():
        default_cookiefile = os.path.join(
            os.path.expanduser("~"), ".mozilla", "firefox", "*", "cookies.sqlite"
        )
        cookiefiles = glob.glob(default_cookiefile)
        if not cookiefiles:
            raise FileNotFoundError("No Firefox cookies.sqlite file found.")
        return max(cookiefiles, key=os.path.getmtime)

    @staticmethod
    def import_session(cookiefile):
        os.makedirs(Firefox.SESSION_DIR, exist_ok=True)
        copied_cookiefile = os.path.join(Firefox.SESSION_DIR, "cookies.sqlite")
        shutil.copyfile(cookiefile, copied_cookiefile)
        print(f"Using cookies from {copied_cookiefile}.")

        conn = sqlite3.connect(f"file:{copied_cookiefile}?immutable=1", uri=True)
        try:
            cookie_data = conn.execute(
                "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
            ).fetchall()
        except sqlite3.OperationalError:
            cookie_data = conn.execute(
                "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
            ).fetchall()

        instaloader = Instaloader(max_connection_attempts=1)
        instaloader.context._session.cookies.update(cookie_data)
        username = instaloader.test_login()

        if not username:
            raise ValueError(
                "Not logged in. Are you logged in successfully in Firefox?"
            )

        print(f"Imported session cookie for {username}.")
        instaloader.context.username = username
        instaloader.save_session_to_file(Firefox.SESSION)
        return instaloader

    @staticmethod
    def get_session():
        if not os.path.exists(Firefox.SESSION):
            cookiefile = Firefox.get_cookiefile()
            instaloader = Firefox.import_session(cookiefile)
        else:
            instaloader = Instaloader(max_connection_attempts=1)
            instaloader.load_session_from_file(username=None, filename=Firefox.SESSION)
        return instaloader
