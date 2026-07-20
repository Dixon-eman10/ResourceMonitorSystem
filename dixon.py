import threading
import random
import time
import requests

BASE_URL = "http://127.0.0.1:5000"

# Normal pages visited by legitimate users
PAGES = [
    "/",
    "/login",
    "/profile",
    "/search"
]

# Realistic number of users
USERS = 20

# Users spend time reading pages
MIN_DELAY = 2
MAX_DELAY = 5


def normal_user(user_id):

    session = requests.Session()

    while True:

        page = random.choice(PAGES)

        try:

            response = session.get(
                BASE_URL + page,
                timeout=5
            )

            print(
                f"[User {user_id:02d}] "
                f"{page:<10} "
                f"{response.status_code}"
            )

        except Exception as e:

            print(f"[User {user_id:02d}] {e}")

        # Simulate a real user reading the page
        time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))


def main():

    print("=" * 60)
    print("LEGITIMATE USER TRAFFIC SIMULATION")
    print("=" * 60)
    print(f"Users          : {USERS}")
    print(f"Think Time     : {MIN_DELAY}-{MAX_DELAY} sec")
    print("=" * 60)

    for i in range(USERS):

        thread = threading.Thread(
            target=normal_user,
            args=(i + 1,),
            daemon=True
        )

        thread.start()

        # Users don't all arrive simultaneously
        time.sleep(0.2)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()