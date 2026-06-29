import threading
import time
from flask import g

from monitoring import metrics


def register_request_tracker(app):
    """
    Registers Flask hooks for tracking requests
    and measuring response time.
    """

    @app.before_request
    def before_request():
        g.start_time = time.time()
        metrics.request_count += 1

    @app.after_request
    def after_request(response):
        response_time = time.time() - g.start_time

        metrics.last_response_time = response_time

        return response


def calculate_request_rate():
    """
    Runs forever in the background and calculates
    requests per second.
    """

    while True:
        time.sleep(1)

        metrics.request_rate = metrics.request_count

        metrics.request_count = 0


def start_request_tracker():
    """
    Starts the background thread.
    """

    tracker_thread = threading.Thread(
        target=calculate_request_rate,
        daemon=True
    )

    tracker_thread.start()