"""
Request Tracker

Tracks:
- Request rate
- Last response time
- Maximum response time
- Average response time
"""

import threading
import time

from flask import g

from monitoring import metrics


# ==========================================================
# Register Flask Hooks
# ==========================================================

def register_request_tracker(app):
    """
    Register request hooks.
    """

    @app.before_request
    def before_request():
        g.start_time = time.perf_counter()

        metrics.request_count += 1

    @app.after_request
    def after_request(response):

        response_time = time.perf_counter() - g.start_time

        if response_time < 0.001:
            response_time = 0.001

        response_time = round(response_time, 3)

        # Last request
        metrics.last_response_time = response_time

        # Running total for average
        metrics.response_total += response_time
        metrics.response_samples += 1

        # Highest response time seen this second
        if response_time > metrics.max_response_time:
            metrics.max_response_time = response_time

        return response


# ==========================================================
# Background Statistics
# ==========================================================

def calculate_request_rate():
    """
    Every second:
    - Calculate request rate
    - Calculate average response time
    - Preserve the maximum response time
    """

    while True:

        time.sleep(1)

        metrics.request_rate = metrics.request_count

        if metrics.response_samples > 0:

            metrics.average_response_time = round(
                metrics.response_total /
                metrics.response_samples,
                3
            )

        else:

            metrics.average_response_time = 0.0

        # Reset counters for next second
        metrics.request_count = 0
        metrics.response_total = 0.0
        metrics.response_samples = 0

        # IMPORTANT:
        # Do NOT reset max_response_time here.
        # The Resource Monitor will read it first and then clear it.


# ==========================================================
# Start Tracker
# ==========================================================

def start_request_tracker():

    tracker_thread = threading.Thread(
        target=calculate_request_rate,
        daemon=True,
        name="RequestTracker"
    )

    tracker_thread.start()